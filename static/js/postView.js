let cross = document.getElementById('cross');
let responseBtn = document.getElementById('response');
let responseContainer = document.getElementById('response-container');
let deleteBtn = document.querySelector('.delete');
let applyBtn = document.querySelector('.apply');
let backgroundBlur = document.querySelector('.background-blur');

if (responseBtn != null) {
    responseBtn.addEventListener("click", () => {
        backgroundBlur.style.display = 'block';
        responseContainer.style.display = 'block';
    });
}

if (cross != null) {
    cross.addEventListener("click", () => {
        backgroundBlur.style.display = 'none';
        responseContainer.style.display = 'none';
    });
}

let print = document.getElementById('print');
if (print != null) {
    print.addEventListener("click", () => {
        var printWindow = window.open('', '', 'width=1200,height=800');
        printWindow.document.open();
        printWindow.document.write('<html><head><title>JobPortal Response post_id={{post.id}}</title></head><body>');
        printWindow.document.write('<div style="margin: 20px;">');
        printWindow.document.write(responseContainer.innerHTML);
        printWindow.document.write('</div></body></html>');
        printWindow.document.close();
        printWindow.print();
        printWindow.close();
    });
}

if (deleteBtn != null) {
    deleteBtn.addEventListener("click", () => {
        backgroundBlur.style.display = 'block';
        document.getElementById('alert').style.display = 'block';
        document.getElementById('alertHeading').innerHTML = 'Alert Message!!!';
        document.getElementById('alertPara').innerHTML = 'Are you sure you want to delete post?';
    });
}

let cancel = document.getElementById('cancel');
if (cancel != null) {
    cancel.addEventListener("click", () => {
        document.getElementById('alert').style.display = 'none';
        backgroundBlur.style.display = 'none';
    });
}

let okay = document.getElementById('okay');
if (okay != null) {
    okay.addEventListener("click", () => {
        document.getElementById('alert').style.display = 'none';
        backgroundBlur.style.display = 'none';
    });
}


if (applyBtn != null) {
    applyBtn.addEventListener("click", () => {
        backgroundBlur.style.display = 'block';
        document.getElementById('apply-alert').style.display = 'block';
        document.getElementById('applyAlertHeading').innerHTML = 'Alert Message!!!';
        document.getElementById('applyAlertPara').innerHTML = 'Are you sure you want to apply to this job?';
    });
}

let applyCancel = document.getElementById('apply-cancel');
if (applyCancel != null) {
    applyCancel.addEventListener("click", () => {
        document.getElementById('apply-alert').style.display = 'none';
        backgroundBlur.style.display = 'none';
    });
}

let applyOkay = document.getElementById('apply-okay');
if (applyOkay != null) {
    applyOkay.addEventListener("click", () => {
        document.getElementById('apply-alert').style.display = 'none';
        backgroundBlur.style.display = 'none';
    });
}

let dummeSubmit = document.getElementById('dummeSubmit');
if (dummeSubmit != null) {
    dummeSubmit.addEventListener("click", () => {
        document.getElementById('mainSubmit').click()
    });
}

backgroundBlur.addEventListener("click", () => {
    document.getElementById('alert').style.display = 'none';
    document.getElementById('apply-alert').style.display = 'none';
    responseContainer.style.display = 'none';
    backgroundBlur.style.display = 'none';
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