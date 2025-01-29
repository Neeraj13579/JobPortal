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


profileImage.addEventListener('mouseover', () => {
    profileImage.style.transform = 'scale(1.1)';
});

profileImage.addEventListener('mouseout', () => {
    profileImage.style.transform = 'scale(1)';
});