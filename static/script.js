$(document).ready(function () {
    $('#chat_form').on('submit', function (event) {
        event.preventDefault();
        var userMessage = $('#user_input').val();
        $('#user_input').val('');
        if (userMessage.trim() !== '') {
            showMessage('user', userMessage);
            sendMessage(userMessage);
        }
    });

    function showLatest() {
        $('#chat_log').scrollTop($('#chat_log')[0].scrollHeight);
    }

    function showMessage(sender, message) {
        var messageElement = $('<div class="message ' + sender + '-message"></div>').html(message.replace(/\n/g, '<br>'));;
        $('#chat_log').append(messageElement);
        showLatest();
    }

    
    function sendMessage(message) {
        showMessage('bot', 'Marc is thinking...');
        $.ajax({
            type: 'POST',
            url: '/chat_with_bot',
            data: { user_input: message },
            success: function (response) {
                $('.bot-message').last().remove();
                showMessage('bot', response.response);
            },
            error: function () {
                $('.bot-message').last().remove();
                showMessage('bot', 'Ouch, I collapsed.');
            }
        });
    }
});