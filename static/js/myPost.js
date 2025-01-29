let classSkills = document.querySelectorAll('.skills');
let deleteBtn = document.querySelectorAll('.delete');

for (let i = 0; i < classSkills.length; i++) {
    let result = '';
    let skills = classSkills[i].innerHTML;
    skill = skills.split(',');
    for (let j = 0; j < skill.length; j++) {
        result = result + skill[j] + " • ";
    }
    classSkills[i].innerHTML = result.slice(0, -2);
}


for (let i = 0; i < deleteBtn.length; i++) {
    deleteBtn[i].addEventListener("click", () => {
        document.querySelector('.background-blur').style.display = 'block';
        document.getElementById('alert').style.display = 'block';
        document.getElementById('alertHeading').innerHTML = 'Alert Message!!!';
        document.getElementById('alertPara').innerHTML = 'Are you sure you want to delete post?';
    });
}

document.getElementById('cancel').addEventListener("click", () => {
    document.getElementById('alert').style.display = 'none';
    document.querySelector('.background-blur').style.display = 'none';
});
document.getElementById('okay').addEventListener("click", () => {
    document.querySelector('.background-blur').style.display = 'none';
});