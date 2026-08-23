(function () {
    'use strict';

    const configElement = document.getElementById('exam-config');

    if (!configElement) {
        return;
    }

    const config = JSON.parse(configElement.textContent);

    let current = 0;
    let remaining = Number(config.remainingSeconds) || 0;
    let editable = Boolean(config.editable);

    /*
     * Time tracking
     *
     * pendingTimeSpent stores seconds that have not yet been
     * successfully persisted by the server.
     */
    let pendingTimeSpent = 0;
    let questionStartTime = Date.now();

    let saveTimeout = null;
    let saveInProgress = false;
    let saveQueued = false;

    let lastAnswerChangeTime = 0;

    const IDLE_THRESHOLD_SECONDS =
        Number(config.idleThresholdSeconds) || 300;

    const RAPID_ANSWER_THRESHOLD_SECONDS =
        Number(config.rapidAnswerThresholdSeconds) || 2;

    const TIMER_WARNING_SECONDS =
        Number(config.timerWarningSeconds) || 300;

    const TIMER_CRITICAL_SECONDS =
        Number(config.timerCriticalSeconds) || 60;

    const AUTOSAVE_SYNC_SECONDS =
        Number(config.autosaveSyncSeconds) || 30;


    // ------------------------------------------------------------
    // DOM helpers
    // ------------------------------------------------------------

    const timerDisplay = document.getElementById('timer-display');
    const warningBox = document.getElementById('exam-warning');
    const progressDisplay = document.getElementById('q-progress');
    const questionText = document.getElementById('q-text');
    const optionsContainer = document.getElementById('q-options');
    const palette = document.getElementById('palette');
    const saveStatus = document.getElementById('save-status');
    const previousButton = document.getElementById('btn-prev');
    const nextButton = document.getElementById('btn-next');
    const reviewButton = document.getElementById('btn-review');
    const questionPanel = document.getElementById('question-panel');


    // ------------------------------------------------------------
    // CSRF
    // ------------------------------------------------------------

    function getCookie(name) {
        const cookies = document.cookie
            ? document.cookie.split('; ')
            : [];

        for (const cookie of cookies) {
            const separatorIndex = cookie.indexOf('=');

            if (separatorIndex === -1) {
                continue;
            }

            const key = cookie.substring(0, separatorIndex);
            const value = cookie.substring(separatorIndex + 1);

            if (key === name) {
                return decodeURIComponent(value);
            }
        }

        return null;
    }


    function csrfToken() {
        return getCookie('csrftoken');
    }


    // ------------------------------------------------------------
    // HTTP helpers
    // ------------------------------------------------------------

    async function postJSON(url, data) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken(),
            },
            credentials: 'same-origin',
            body: JSON.stringify(data),
        });

        let responseData = {};

        try {
            responseData = await response.json();
        } catch (error) {
            responseData = {
                success: false,
                error: 'Invalid server response.',
            };
        }

        return {
            ok: response.ok,
            status: response.status,
            data: responseData,
        };
    }


    async function getJSON(url) {
        const response = await fetch(url, {
            method: 'GET',
            credentials: 'same-origin',
            headers: {
                'Accept': 'application/json',
            },
        });

        let responseData = {};

        try {
            responseData = await response.json();
        } catch (error) {
            responseData = {
                success: false,
                error: 'Invalid server response.',
            };
        }

        return {
            ok: response.ok,
            status: response.status,
            data: responseData,
        };
    }


    // ------------------------------------------------------------
    // UI helpers
    // ------------------------------------------------------------

    function setStatus(text) {
        if (saveStatus) {
            saveStatus.textContent = text;
        }
    }


    function showWarning(text) {
        if (!warningBox) {
            return;
        }

        warningBox.textContent = '⚠ ' + text;
        warningBox.classList.remove('d-none');
    }


    function hideWarning() {
        if (!warningBox) {
            return;
        }

        warningBox.textContent = '';
        warningBox.classList.add('d-none');
    }


    function formatTime(seconds) {
        seconds = Math.max(0, Math.floor(seconds));

        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;

        return (
            String(minutes).padStart(2, '0') +
            ':' +
            String(remainingSeconds).padStart(2, '0')
        );
    }


    function updateTimerDisplay() {
        if (!timerDisplay) {
            return;
        }

        timerDisplay.textContent = formatTime(remaining);

        timerDisplay.classList.remove(
            'text-warning',
            'text-danger'
        );

        if (remaining <= TIMER_CRITICAL_SECONDS) {
            timerDisplay.classList.add('text-danger');
        } else if (remaining <= TIMER_WARNING_SECONDS) {
            timerDisplay.classList.add('text-warning');
        }
    }


    function setInterfaceEditable(value) {
        editable = Boolean(value);

        if (previousButton) {
            previousButton.disabled = !editable;
        }

        if (nextButton) {
            nextButton.disabled = !editable;
        }

        if (reviewButton) {
            reviewButton.disabled = !editable;
        }

        if (optionsContainer) {
            optionsContainer
                .querySelectorAll('input[type="radio"]')
                .forEach(input => {
                    input.disabled = !editable;
                });
        }

        if (!editable) {
            showWarning(
                'This attempt is no longer editable.'
            );
        }
        updateNavigationButtons();
    }


    // ------------------------------------------------------------
    // Question time tracking
    // ------------------------------------------------------------

    function collectCurrentQuestionTime() {
        const elapsed = Math.floor(
            (Date.now() - questionStartTime) / 1000
        );

        if (elapsed > 0) {
            pendingTimeSpent += elapsed;
            questionStartTime = Date.now();
        }
    }


    function resetQuestionTimer() {
        questionStartTime = Date.now();
    }


    // ------------------------------------------------------------
    // Rendering
    // ------------------------------------------------------------

    function render() {
        const question = config.questions[current];

        if (!question) {
            return;
        }

        if (progressDisplay) {
            progressDisplay.textContent =
                `Question ${current + 1} of ${config.questions.length}`;
        }

        if (questionText) {
            questionText.textContent = question.text;
        }

        if (optionsContainer) {
            optionsContainer.innerHTML = '';

            ['A', 'B', 'C', 'D'].forEach(option => {
                const wrapper = document.createElement('div');
                wrapper.className = 'form-check mb-2';

                const input = document.createElement('input');

                input.className = 'form-check-input';
                input.type = 'radio';
                input.name = 'option';
                input.id = `option-${option}`;
                input.value = option;
                input.checked =
                    question.selected_option === option;
                input.disabled = !editable;

                const label = document.createElement('label');

                label.className = 'form-check-label';
                label.htmlFor = input.id;
                label.textContent =
                    `${option}. ${question.options[option]}`;

                input.addEventListener(
                    'change',
                    onAnswerChange
                );

                wrapper.appendChild(input);
                wrapper.appendChild(label);

                optionsContainer.appendChild(wrapper);
            });
        }

        if (reviewButton) {
            reviewButton.textContent =
                question.marked_for_review
                    ? 'Unmark Review'
                    : 'Mark for Review';
        }

        renderPalette();

        resetQuestionTimer();
        updateNavigationButtons();
    }


    function renderPalette() {
        if (!palette) {
            return;
        }

        palette.innerHTML = '';

        config.questions.forEach((question, index) => {
            const button = document.createElement('button');

            button.type = 'button';
            button.dataset.index = index;

            let className = 'btn btn-sm ';

            if (index === current) {
                className += 'btn-primary';
            } else if (question.marked_for_review) {
                className += 'btn-warning';
            } else if (question.selected_option) {
                className += 'btn-success';
            } else {
                className += 'btn-outline-secondary';
            }

            button.className = className;
            button.textContent = index + 1;
            button.disabled = !editable;

            button.addEventListener('click', function () {
                goTo(index);
            });

            palette.appendChild(button);
        });
    }


    function updateNavigationButtons() {
        if (previousButton) {
            previousButton.disabled =
                !editable || current === 0;
        }

        if (nextButton) {
            nextButton.disabled =
                !editable ||
                current === config.questions.length - 1;
        }
    }


    // ------------------------------------------------------------
    // Answer persistence
    // ------------------------------------------------------------

    function onAnswerChange(event) {
        if (!editable) {
            return;
        }

        const question = config.questions[current];

        question.selected_option = event.target.value;

        const now = Date.now();

        if (
            lastAnswerChangeTime > 0 &&
            (now - lastAnswerChangeTime) / 1000
                <= RAPID_ANSWER_THRESHOLD_SECONDS
        ) {
            logSecurityEvent('rapid_answer');
        }

        lastAnswerChangeTime = now;

        scheduleSave();
        renderPalette();
    }


    function scheduleSave() {
        if (!editable) {
            return;
        }

        clearTimeout(saveTimeout);

        setStatus('Saving...');

        saveTimeout = setTimeout(
            saveCurrentQuestion,
            300
        );
    }


    async function saveCurrentQuestion() {
        if (!editable) {
            return false;
        }

        const question = config.questions[current];

        if (!question) {
            return false;
        }

        collectCurrentQuestionTime();

        if (saveInProgress) {
            saveQueued = true;
            return false;
        }

        saveInProgress = true;

        const timeToSend = pendingTimeSpent;

        setStatus('Saving...');

        try {
            const result = await postJSON(
                config.answerUrl,
                {
                    question_id: question.question_id,
                    selected_option:
                        question.selected_option || null,
                    marked_for_review:
                        Boolean(question.marked_for_review),
                    time_spent: timeToSend,
                }
            );

            if (result.data.success) {
                /*
                 * Only clear the amount that was actually sent.
                 *
                 * If additional time accumulated while the
                 * request was in progress, it remains pending.
                 */
                pendingTimeSpent =
                    Math.max(
                        0,
                        pendingTimeSpent - timeToSend
                    );

                setStatus('Saved');

                return true;
            }

            if (result.status === 409) {
                editable = false;
                setInterfaceEditable(false);

                setStatus('Attempt closed');

                return false;
            }

            setStatus('Save failed');

            return false;

        } catch (error) {
            setStatus(
                'Connection issue — answer not yet saved'
            );

            return false;

        } finally {
            saveInProgress = false;

            if (saveQueued) {
                saveQueued = false;

                if (editable) {
                    scheduleSave();
                }
            }
        }
    }


    // ------------------------------------------------------------
    // Navigation
    // ------------------------------------------------------------

    async function goTo(index) {
        if (
            !editable ||
            index < 0 ||
            index >= config.questions.length ||
            index === current
        ) {
            return;
        }

        collectCurrentQuestionTime();

        await saveCurrentQuestion();

        if (!editable) {
            return;
        }

        current = index;

        render();
    }


    // ------------------------------------------------------------
    // Review
    // ------------------------------------------------------------

    async function toggleReview() {
        if (!editable) {
            return;
        }

        const question = config.questions[current];

        question.marked_for_review =
            !question.marked_for_review;

        renderPalette();

        if (reviewButton) {
            reviewButton.textContent =
                question.marked_for_review
                    ? 'Unmark Review'
                    : 'Mark for Review';
        }

        await saveCurrentQuestion();
    }


    // ------------------------------------------------------------
    // Timer
    // ------------------------------------------------------------

    function tickTimer() {
        if (!editable) {
            updateTimerDisplay();
            return;
        }

        remaining = Math.max(
            0,
            remaining - 1
        );

        updateTimerDisplay();

        if (remaining <= 0) {
            setInterfaceEditable(false);

            showWarning(
                'Time is up. This attempt is no longer editable.'
            );

            /*
             * Do not pretend that this performs server-side
             * submission. The server remains authoritative.
             *
             * The submission/auto-submit endpoint will be
             * implemented in the submission step.
             */
        }
    }


    async function syncTimer() {
        try {
            const result =
                await getJSON(config.timerUrl);

            if (!result.ok) {
                return;
            }

            const data = result.data;

            if (
                typeof data.remaining_seconds ===
                'number'
            ) {
                remaining =
                    Math.max(
                        0,
                        data.remaining_seconds
                    );
            }

            if (
                typeof data.editable ===
                'boolean'
            ) {
                setInterfaceEditable(
                    data.editable
                );
            }

            updateTimerDisplay();

            if (
                typeof data.attempt_status ===
                'string' &&
                data.attempt_status !==
                'in_progress'
            ) {
                setInterfaceEditable(false);
            }

        } catch (error) {
            /*
             * Do not stop the local timer merely because
             * synchronization temporarily failed.
             */
        }
    }


    // ------------------------------------------------------------
    // Security / anti-cheat event logging
    // ------------------------------------------------------------

    async function logSecurityEvent(eventType) {
        try {
            await postJSON(
                config.securityUrl,
                {
                    event_type: eventType,
                }
            );
        } catch (error) {
            /*
             * Security telemetry failure must not crash
             * the examination interface.
             */
        }
    }


    // Tab/window visibility
    document.addEventListener(
        'visibilitychange',
        function () {
            if (document.hidden) {
                logSecurityEvent('tab_switch');

                showWarning(
                    'Leaving the exam window has been detected. ' +
                    'This activity has been recorded.'
                );
            }
        }
    );


    // Fullscreen exit
    document.addEventListener(
        'fullscreenchange',
        function () {
            if (!document.fullscreenElement) {
                logSecurityEvent(
                    'fullscreen_exit'
                );
            }
        }
    );


    // Copy
    if (questionPanel) {
        questionPanel.addEventListener(
            'copy',
            function (event) {
                event.preventDefault();

                logSecurityEvent(
                    'copy_attempt'
                );
            }
        );


        // Paste
        questionPanel.addEventListener(
            'paste',
            function (event) {
                event.preventDefault();

                logSecurityEvent(
                    'paste_attempt'
                );
            }
        );


        // Right click
        questionPanel.addEventListener(
            'contextmenu',
            function (event) {
                event.preventDefault();

                logSecurityEvent(
                    'right_click'
                );
            }
        );
    }


    // ------------------------------------------------------------
    // Idle detection
    // ------------------------------------------------------------

    let lastActivityTime = Date.now();
    let idleLogged = false;

    [
        'mousemove',
        'keydown',
        'click',
        'touchstart',
    ].forEach(eventName => {
        document.addEventListener(
            eventName,
            function () {
                lastActivityTime = Date.now();
                idleLogged = false;
            }
        );
    });


    setInterval(function () {
        if (!editable || idleLogged) {
            return;
        }

        const idleSeconds =
            (Date.now() - lastActivityTime) / 1000;

        if (
            idleSeconds >=
            IDLE_THRESHOLD_SECONDS
        ) {
            logSecurityEvent('idle');

            idleLogged = true;
        }
    }, 10000);


    // ------------------------------------------------------------
    // Fullscreen button
    // ------------------------------------------------------------

    if (questionPanel) {
        const fullscreenButton =
            document.createElement('button');

        fullscreenButton.type = 'button';
        fullscreenButton.textContent =
            'Enter Fullscreen';

        fullscreenButton.className =
            'btn btn-outline-primary btn-sm mb-2';

        fullscreenButton.addEventListener(
            'click',
            function () {
                if (
                    document.documentElement
                        .requestFullscreen
                ) {
                    document.documentElement
                        .requestFullscreen()
                        .catch(() => {});
                }
            }
        );

        questionPanel.prepend(
            fullscreenButton
        );
    }


    // ------------------------------------------------------------
    // Button event handlers
    // ------------------------------------------------------------

    if (previousButton) {
        previousButton.addEventListener(
            'click',
            function () {
                goTo(current - 1);
            }
        );
    }


    if (nextButton) {
        nextButton.addEventListener(
            'click',
            function () {
                goTo(current + 1);
            }
        );
    }


    if (reviewButton) {
        reviewButton.addEventListener(
            'click',
            toggleReview
        );
    }


    // ------------------------------------------------------------
    // Initialization
    // ------------------------------------------------------------

    render();
    updateTimerDisplay();

    setInterval(
        tickTimer,
        1000
    );

    setInterval(
        syncTimer,
        AUTOSAVE_SYNC_SECONDS * 1000
    );

})();