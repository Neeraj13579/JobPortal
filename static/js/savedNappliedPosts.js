let classSkills = document.querySelectorAll('.skills');

for (let i = 0; i < classSkills.length; i++) {
    let result = '';
    let skills = classSkills[i].innerHTML;

    skill = skills.split(',');

    for (let j = 0; j < skill.length; j++) {
        result = result + skill[j] + " • ";
    }
    classSkills[i].innerHTML = result.slice(0, -2);
}

$(document).ready(function () {
    $('.save-unsave-button').click(function () {
        var postId = $(this).data('post-id');
        var button = $(this);

        $.ajax({
            url: '/save_unsave_post/' + postId,
            method: 'GET',
            success: function (data) {
                if (data.saved) {
                    button.removeClass('save').addClass('unsave');
                    button.html('<i class="fa-solid fa-bookmark"></i> Unsave');
                } else {
                    button.removeClass('unsave').addClass('save');
                    button.html('<i class="fa-regular fa-bookmark"></i> Save');
                }
            },
            error: function (error) {
                console.error('Ajax request failed:', error);
            }
        });
    });
});