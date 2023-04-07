const sections = document.getElementsByClassName("section-1-middle");
const leftBtn = document.getElementsByClassName("section-1-left")[0];
const rightBtn = document.getElementsByClassName("section-1-right")[0];
let sectionIndex = 0;


console.log("Total sections: ", sections.length)
for (let i = 1; i < sections.length; i++) {
    sections[i].style.display = 'none';
}

rightBtn.addEventListener('click', () => {
    sections[sectionIndex].style.display = 'none';
    if (sectionIndex <= 2) sectionIndex++;
    else sectionIndex = 1;
    sections[sectionIndex].style.display = "block";
    console.log("current section: ", sectionIndex)
})

leftBtn.addEventListener('click', () => {
    sections[sectionIndex].style.display = 'none';
    if (sectionIndex >= 0) sectionIndex--;
    else sectionIndex = 2;
    sections[sectionIndex].style.display = "block";
    console.log("current section: ", sectionIndex)
})