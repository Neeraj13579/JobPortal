let hirerCompanyData = document.getElementById('hirerCompanyData');
let hirerCompanyDetailData = document.getElementById('hirerCompanyDetailData');
let hirerAddressData = document.getElementById('hirerAddressData');
let hirerSocialData = document.getElementById('hirerSocialData');

let radio = document.getElementsByName('menu');
for (let i = 0; i < radio.length; i++) {
    radio[i].addEventListener("click", () => {
        if (radio[i].id == 'companyDetails') {
            hirerCompanyData.style.display = 'block';
            hirerCompanyDetailData.style.display = 'none';
            hirerAddressData.style.display = 'none';
            hirerSocialData.style.display = 'none';
        }
        else if (radio[i].id == 'companyMoreDetails') {
            hirerCompanyData.style.display = 'none';
            hirerCompanyDetailData.style.display = 'block';
            hirerAddressData.style.display = 'none';
            hirerSocialData.style.display = 'none';
        }
        else if (radio[i].id == 'companyAddress') {
            hirerCompanyData.style.display = 'none';
            hirerCompanyDetailData.style.display = 'none';
            hirerAddressData.style.display = 'block';
            hirerSocialData.style.display = 'none';
        }
        else {
            hirerCompanyData.style.display = 'none';
            hirerCompanyDetailData.style.display = 'none';
            hirerAddressData.style.display = 'none';
            hirerSocialData.style.display = 'block';
        }
    });
}

let edit = document.getElementsByClassName('edit');
let submit = document.getElementsByClassName('submit');

let profileForm = document.getElementsByClassName('profileForm');
let companyForm = document.getElementsByClassName('companyForm');
let addressForm = document.getElementsByClassName('addressForm');
let socialForm = document.getElementsByClassName('socialForm');

for (let i = 0; i < edit.length; i++) {
    edit[i].addEventListener("click", () => {
        edit[i].style.display = 'none';
        submit[i].style.display = 'block';
        if (i == 0) {
            for (var j = 0; j < profileForm.length; j++) {
                profileForm[j].removeAttribute('disabled');
                profileForm[j].classList.add('bg');
                profileForm[j].classList.remove('nobg');
            }
        }
        else if (i == 1) {
            for (var j = 0; j < companyForm.length; j++) {
                companyForm[j].removeAttribute('disabled');
                companyForm[j].classList.add('bg');
                companyForm[j].classList.remove('nobg');
            }
        }
        else if (i == 2) {
            for (var j = 0; j < addressForm.length; j++) {
                addressForm[j].removeAttribute('disabled');
                addressForm[j].classList.add('bg');
                addressForm[j].classList.remove('nobg');
            }
        }
        else {
            for (var j = 0; j < socialForm.length; j++) {
                socialForm[j].removeAttribute('disabled');
                socialForm[j].classList.add('bg');
                socialForm[j].classList.remove('nobg');
            }
        }
    });
}

const profileImage = document.getElementById('profile-img');
const imageInput = document.getElementById('imageInput');
const profileImgForm = document.getElementById('profileImgForm');
const formImgSubmit = document.getElementById('form_img');


profileImage.addEventListener('mouseover', () => {
    profileImage.style.transform = 'scale(1.1)';
});

profileImage.addEventListener('mouseout', () => {
    profileImage.style.transform = 'scale(1)';
});

profileImage.addEventListener('click', () => {
    imageInput.click();
});

imageInput.addEventListener('change', () => {
    formImgSubmit.click();
});