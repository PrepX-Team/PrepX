document.addEventListener(
    'DOMContentLoaded',
    function () {

        /* =====================================================
           SECURITY EVENT URL
           ===================================================== */

        const securityEventUrl =
            window.PREPX_SECURITY_EVENT_URL;


        /* =====================================================
           STATE
           ===================================================== */

        let focusLost = false;


        /* =====================================================
           LOG SECURITY EVENT
           ===================================================== */

        function logSecurityEvent(eventType) {

            if (!securityEventUrl) {

                console.error(
                    'Security event URL is not configured.'
                );

                return;

            }


            const csrfTokenElement =
                document.querySelector(
                    '[name=csrfmiddlewaretoken]'
                );


            const csrfToken =
                csrfTokenElement
                    ? csrfTokenElement.value
                    : '';


            const formData =
                new FormData();


            formData.append(
                'event_type',
                eventType
            );


            fetch(
                securityEventUrl,
                {
                    method: 'POST',

                    headers: {
                        'X-CSRFToken':
                            csrfToken,
                    },

                    body: formData,

                    credentials: 'same-origin',
                }
            )

            .then(
                function (response) {

                    if (!response.ok) {

                        throw new Error(
                            'Security event request failed: ' +
                            response.status
                        );

                    }

                    return response.json();

                }
            )

            .then(
                function (data) {

                    if (data.success) {

                        console.log(
                            'Security event logged:',
                            eventType
                        );

                    }

                    else {

                        console.error(
                            'Security event failed:',
                            data.error
                        );

                    }

                }
            )

            .catch(
                function (error) {

                    console.error(
                        'Security event error:',
                        error
                    );

                }
            );

        }


        /* =====================================================
           HANDLE FOCUS LOSS
           ===================================================== */

        function handleFocusLoss() {

            /*
             * Prevent duplicate violation when
             * blur and visibilitychange happen together.
             */

            if (focusLost) {

                return;

            }


            focusLost = true;


            /*
             * Count only one violation.
             */

            logSecurityEvent(
                'tab_switch'
            );

        }


        /* =====================================================
           TAB VISIBILITY CHANGE
           ===================================================== */

        document.addEventListener(
            'visibilitychange',
            function () {

                if (
                    document.visibilityState ===
                    'hidden'
                ) {

                    handleFocusLoss();

                }

                else {

                    focusLost = false;

                }

            }
        );


        /* =====================================================
           WINDOW BLUR
           ===================================================== */

        window.addEventListener(
            'blur',
            function () {

                handleFocusLoss();

            }
        );


        /* =====================================================
           WINDOW FOCUS
           ===================================================== */

        window.addEventListener(
            'focus',
            function () {

                focusLost = false;

            }
        );


        /* =====================================================
           COPY PROTECTION
           ===================================================== */

        document.addEventListener(
            'copy',
            function (event) {

                /*
                 * Prevent copying exam content.
                 */

                event.preventDefault();


                /*
                 * Log copy attempt.
                 */

                logSecurityEvent(
                    'copy_attempt'
                );

            }
        );


        /* =====================================================
           PASTE PROTECTION
           ===================================================== */

        document.addEventListener(
            'paste',
            function (event) {

                /*
                 * Prevent pasting into exam.
                 */

                event.preventDefault();


                /*
                 * Log paste attempt.
                 */

                logSecurityEvent(
                    'paste_attempt'
                );

            }
        );


        /* =====================================================
           RIGHT CLICK PROTECTION
           ===================================================== */
        /* =====================================================
   RIGHT CLICK PROTECTION
   ===================================================== */

        document.addEventListener(
            'contextmenu',
            function (event) {

                /*
                * Disable browser context menu.
                *
                * Right-click is NOT counted
                * as a security violation.
                */

                event.preventDefault();

            }
        );
       


        /* =====================================================
           KEYBOARD SHORTCUT PROTECTION
           ===================================================== */

        document.addEventListener(
            'keydown',
            function (event) {

                /*
                 * Ctrl + C
                 */

                if (
                    event.ctrlKey &&
                    event.key.toLowerCase() === 'c'
                ) {

                    event.preventDefault();

                    logSecurityEvent(
                        'keyboard_attempt'
                    );

                    return;

                }


                /*
                 * Ctrl + V
                 */

                if (
                    event.ctrlKey &&
                    event.key.toLowerCase() === 'v'
                ) {

                    event.preventDefault();

                    logSecurityEvent(
                        'keyboard_attempt'
                    );

                    return;

                }


                /*
                 * Ctrl + X
                 */

                if (
                    event.ctrlKey &&
                    event.key.toLowerCase() === 'x'
                ) {

                    event.preventDefault();

                    logSecurityEvent(
                        'keyboard_attempt'
                    );

                    return;

                }


                /*
                 * Ctrl + A
                 */

                if (
                    event.ctrlKey &&
                    event.key.toLowerCase() === 'a'
                ) {

                    event.preventDefault();

                    logSecurityEvent(
                        'keyboard_attempt'
                    );

                    return;

                }


                /*
                 * Ctrl + S
                 */

                if (
                    event.ctrlKey &&
                    event.key.toLowerCase() === 's'
                ) {

                    event.preventDefault();

                    logSecurityEvent(
                        'keyboard_attempt'
                    );

                    return;

                }


                /*
                 * F12 Developer Tools
                 */

                if (
                    event.key === 'F12'
                ) {

                    event.preventDefault();

                    logSecurityEvent(
                        'keyboard_attempt'
                    );

                    return;

                }


                /*
                 * Ctrl + Shift + I
                 * Developer Tools
                 */

                if (
                    event.ctrlKey &&
                    event.shiftKey &&
                    event.key.toLowerCase() === 'i'
                ) {

                    event.preventDefault();

                    logSecurityEvent(
                        'keyboard_attempt'
                    );

                    return;

                }


                /*
                 * Ctrl + Shift + J
                 * Browser Console
                 */

                if (
                    event.ctrlKey &&
                    event.shiftKey &&
                    event.key.toLowerCase() === 'j'
                ) {

                    event.preventDefault();

                    logSecurityEvent(
                        'keyboard_attempt'
                    );

                    return;

                }


                /*
                 * Ctrl + U
                 * View Page Source
                 */

                if (
                    event.ctrlKey &&
                    event.key.toLowerCase() === 'u'
                ) {

                    event.preventDefault();

                    logSecurityEvent(
                        'keyboard_attempt'
                    );

                    return;

                }

            }
        );

    }
);