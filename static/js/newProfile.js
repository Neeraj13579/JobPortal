let edit = document.getElementsByClassName('edit');
let submit = document.getElementsByClassName('submit');

let profileForm = document.getElementsByClassName('profileForm');
let technicalForm = document.getElementsByClassName('technicalForm');
let addressForm = document.getElementsByClassName('addressForm');
let educationForm = document.getElementsByClassName('educationForm');
let experienceForm = document.getElementsByClassName('experienceForm');

let dateEdu = document.getElementsByClassName('dateEdu');
let dateTextEdu = document.getElementsByClassName('dateTextEdu');
let dateExp = document.getElementsByClassName('dateExp');
let dateTextExp = document.getElementsByClassName('dateTextExp');
let dateDet = document.getElementById('dateDet');
let dateTextDet = document.getElementById('dateTextDet');

let skillsInput = document.getElementById('skillsInput');
let skillsOutput = document.getElementById('skillsOutput');

let resumeStatus = document.getElementById('resumeStatus');

for (let i = 0; i < edit.length; i++) {
    edit[i].addEventListener("click", () => {
        edit[i].style.display = 'none';
        submit[i].style.display = 'block';
        if (i == 0) {
            for (var j = 0; j < profileForm.length; j++) {
                profileForm[j].removeAttribute('disabled');
                profileForm[j].classList.add('bg');
                profileForm[j].classList.remove('nobg');

                dateTextDet.style.display = 'none';
                dateDet.style.display = 'block';
            }
        }
        else if (i == 1) {
            for (var j = 0; j < technicalForm.length; j++) {
                skillsInput.style.display = 'block';
                skillsOutput.style.display = 'none';

                resumeStatus.innerHTML = '<input class="technicalForm nobg" type="file" accept=".pdf" name="file" id="id_resume" disabled>';

                technicalForm[j].removeAttribute('disabled');
                technicalForm[j].classList.add('bg');
                technicalForm[j].classList.remove('nobg');
            }
        }
        else if (i == 2) {
            for (var j = 0; j < addressForm.length; j++) {
                addressForm[j].removeAttribute('disabled');
                addressForm[j].classList.add('bg');
                addressForm[j].classList.remove('nobg');
            }
        }
        else if (i == 3) {
            for (var j = 0; j < educationForm.length; j++) {
                educationForm[j].removeAttribute('disabled');
                educationForm[j].classList.add('bg');
                educationForm[j].classList.remove('nobg');
                for (var k = 0; k < 2; k++) {
                    dateTextEdu[k].style.display = 'none';
                    dateEdu[k].style.display = 'block';
                }
            }
        }
        else if (i == 4) {
            for (var j = 0; j < experienceForm.length; j++) {
                experienceForm[j].removeAttribute('disabled');
                experienceForm[j].classList.add('bg');
                experienceForm[j].classList.remove('nobg');
                for (var k = 0; k < 2; k++) {
                    dateTextExp[k].style.display = 'none';
                    dateExp[k].style.display = 'block';
                }
            }
        }
        else {
            console.log(Error);
        }
    });
    submit[i].addEventListener("click", () => {
        edit[i].style.display = 'block';
        submit[i].style.display = 'none';
    });
}

let add = document.getElementsByClassName('add');
let inputEdu = document.getElementsByClassName('inputEdu');
let inputExp = document.getElementsByClassName('inputExp');

add[0].addEventListener("click", ()=>{
    document.getElementById('submitEdu').style.display = 'block';
    add[0].style.display = 'none';
    for (let j = 0; j < inputEdu.length; j++) {
        inputEdu[j].style.display = 'block';
    }
});

add[1].addEventListener("click", ()=>{
    document.getElementById('submitExp').style.display = 'block';
    add[1].style.display = 'none';
    for (let j = 0; j < inputExp.length; j++) {
        inputExp[j].style.display = 'block';
    }
});



let radio = document.getElementsByName('menu');
for (let i = 0; i < radio.length; i++) {
    radio[i].addEventListener("click", () => {
        if (radio[i].id == 'basic') {
            document.getElementById("basicData").style.display = 'block';
            document.getElementById("technicalData").style.display = 'none';
            document.getElementById("addressData").style.display = 'none';
            document.getElementById("educationData").style.display = 'none';
            document.getElementById("experienceData").style.display = 'none';
        }
        else if (radio[i].id == 'technical') {
            document.getElementById("basicData").style.display = 'none';
            document.getElementById("technicalData").style.display = 'block';
            document.getElementById("addressData").style.display = 'none';
            document.getElementById("educationData").style.display = 'none';
            document.getElementById("experienceData").style.display = 'none';
        }
        else if (radio[i].id == 'address') {
            document.getElementById("basicData").style.display = 'none';
            document.getElementById("technicalData").style.display = 'none';
            document.getElementById("addressData").style.display = 'block';
            document.getElementById("educationData").style.display = 'none';
            document.getElementById("experienceData").style.display = 'none';
        }
        else if (radio[i].id == 'education') {
            document.getElementById("basicData").style.display = 'none';
            document.getElementById("technicalData").style.display = 'none';
            document.getElementById("addressData").style.display = 'none';
            document.getElementById("educationData").style.display = 'block';
            document.getElementById("experienceData").style.display = 'none';
        }
        else {
            document.getElementById("basicData").style.display = 'none';
            document.getElementById("technicalData").style.display = 'none';
            document.getElementById("addressData").style.display = 'none';
            document.getElementById("educationData").style.display = 'none';
            document.getElementById("experienceData").style.display = 'block';
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