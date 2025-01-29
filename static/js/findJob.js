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
let dept_view_all = document.getElementById('dept-view-all');
let dept_view_less = document.getElementById('dept-view-less');
if (dept_view_all != null) {
    dept_view_all.addEventListener("click", () => {
        document.getElementById('all-department-content').style.display = 'block';
        dept_view_all.style.display = 'none';
    });
}
if (dept_view_less != null) {
    dept_view_less.addEventListener("click", () => {
        document.getElementById('all-department-content').style.display = 'none';
        dept_view_all.style.display = 'block';
    });
}

let loc_view_all = document.getElementById('loc-view-all');
let loc_view_less = document.getElementById('loc-view-less');
if (loc_view_all != null) {
    loc_view_all.addEventListener("click", () => {
        document.getElementById('all-location-content').style.display = 'block';
        loc_view_all.style.display = 'none';
    });
}
if (loc_view_less != null) {
    loc_view_less.addEventListener("click", () => {
        document.getElementById('all-location-content').style.display = 'none';
        loc_view_all.style.display = 'block';
    });
}

let role_view_all = document.getElementById('role-view-all');
let role_view_less = document.getElementById('role-view-less');
if (role_view_all != null) {
    role_view_all.addEventListener("click", () => {
        document.getElementById('all-role-content').style.display = 'block';
        role_view_all.style.display = 'none';
    });
}
if (role_view_less != null) {
    document.getElementById('role-view-less').addEventListener("click", () => {
        document.getElementById('all-role-content').style.display = 'none';
        role_view_all.style.display = 'block';
    });
}


document.getElementById('emp-angle-down').addEventListener("click", () => {
    document.getElementById('emp-angle-down').querySelector('i').classList.toggle('fa-rotate-270');
    if (document.getElementById('emp-angle-down').querySelector('i').classList.contains('fa-rotate-270')) {
        document.querySelector('.employee-type-content').style.display = 'none';
    } else {
        document.querySelector('.employee-type-content').style.display = 'block';

    }
});
document.getElementById('exp-angle-down').addEventListener("click", () => {
    document.getElementById('exp-angle-down').querySelector('i').classList.toggle('fa-rotate-270');
    if (document.getElementById('exp-angle-down').querySelector('i').classList.contains('fa-rotate-270')) {
        document.querySelector('.experience-content').style.display = 'none';
    } else {
        document.querySelector('.experience-content').style.display = 'block';
    }
});
document.getElementById('dept-angle-down').addEventListener("click", () => {
    document.getElementById('dept-angle-down').querySelector('i').classList.toggle('fa-rotate-270');
    if (document.getElementById('dept-angle-down').querySelector('i').classList.contains('fa-rotate-270')) {
        document.querySelector('.top-department-content').style.display = 'none';
        document.getElementById('all-department-content').style.display = 'none';
    } else {
        document.querySelector('.top-department-content').style.display = 'block';
        document.getElementById('dept-view-all').style.display = 'block';
    }
});
document.getElementById('loc-angle-down').addEventListener("click", () => {
    document.getElementById('loc-angle-down').querySelector('i').classList.toggle('fa-rotate-270');
    if (document.getElementById('loc-angle-down').querySelector('i').classList.contains('fa-rotate-270')) {
        document.getElementById('top-location-content').style.display = 'none';
        document.getElementById('all-location-content').style.display = 'none';
    } else {
        document.getElementById('top-location-content').style.display = 'block';
        document.getElementById('loc-view-all').style.display = 'block';
    }
});
document.getElementById('sly-angle-down').addEventListener("click", () => {
    document.getElementById('sly-angle-down').querySelector('i').classList.toggle('fa-rotate-270');
    if (document.getElementById('sly-angle-down').querySelector('i').classList.contains('fa-rotate-270')) {
        document.querySelector('.salary-content').style.display = 'none';
    } else {
        document.querySelector('.salary-content').style.display = 'block';
    }
});
document.getElementById('role-angle-down').addEventListener("click", () => {
    document.getElementById('role-angle-down').querySelector('i').classList.toggle('fa-rotate-270');
    if (document.getElementById('role-angle-down').querySelector('i').classList.contains('fa-rotate-270')) {
        document.getElementById('top-role-content').style.display = 'none';
        document.getElementById('all-role-content').style.display = 'none';
    } else {
        document.getElementById('top-role-content').style.display = 'block';
        document.getElementById('role-view-all').style.display = 'block';
    }
});

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

document.querySelectorAll('.reamaining-department-box input').forEach((element) => {
    if (element.checked) {
        document.getElementById('all-department-content').style.display = 'block';
        document.getElementById('dept-view-all').style.display = 'none';
    }
});
document.querySelectorAll('.remaining-location-box input').forEach((element) => {
    if (element.checked) {
        document.getElementById('all-location-content').style.display = 'block';
        document.getElementById('loc-view-all').style.display = 'none';
    }
});
document.querySelectorAll('.remaining-role-box input').forEach((element) => {
    if (element.checked) {
        document.getElementById('all-role-content').style.display = 'block';
        document.getElementById('role-view-all').style.display = 'none';
    }
});


document.addEventListener("DOMContentLoaded", function () {
    // Get the form element
    var form = document.getElementById("myForm");

    // Add a submit event listener to the form
    form.addEventListener("submit", function (event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Serialize the form data into a URL-encoded string
        var formData = new FormData(form);

        // Remove the CSRF token from the serialized data
        formData.delete("csrfmiddlewaretoken");

        // Construct the URL with the modified serialized data
        var formDataString = new URLSearchParams(formData).toString();
        var actionUrl = form.getAttribute("action");
        var finalUrl = actionUrl + "?" + formDataString;

        // Redirect to the constructed URL without actually submitting the form
        window.location.href = finalUrl;
    });
});


let radioInput = document.querySelectorAll('input[type="checkbox"]');
let freshnessInput = document.getElementById('freshness');
let myFilterSubmit = document.getElementById('filterSubmit');
radioInput.forEach((element) => {
    element.addEventListener("input", () => {
        myFilterSubmit.click();
    });
});

freshnessInput.addEventListener("input", () => {
    myFilterSubmit.click();
});