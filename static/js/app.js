document.addEventListener('DOMContentLoaded', function () {

    const subjectField = document.getElementById('id_subject');
    const topicField = document.getElementById('id_topic');

    if (subjectField && topicField) {

        subjectField.addEventListener('change', function () {

            const subjectId = this.value;

            topicField.innerHTML =
                '<option value="">Loading...</option>';

            if (!subjectId) {
                topicField.innerHTML =
                    '<option value="">Select a subject first</option>';
                return;
            }

            fetch(`/subjects/api/topics/?subject_id=${subjectId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to load topics');
                    }

                    return response.json();
                })
                .then(data => {

                    topicField.innerHTML =
                        '<option value="">Select topic</option>';

                    data.forEach(topic => {

                        const option =
                            document.createElement('option');

                        option.value = topic.id;
                        option.textContent = topic.name;

                        topicField.appendChild(option);
                    });
                })
                .catch(error => {

                    console.error(
                        'Error loading topics:',
                        error
                    );

                    topicField.innerHTML =
                        '<option value="">Error loading topics</option>';
                });
        });
    }
});