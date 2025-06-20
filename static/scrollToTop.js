window.onscroll = function () {
    const btn = document.getElementById("scrollTopBtn");
    if (window.scrollY > 200) {
        btn.style.display = "block";
    } else {
        btn.style.display = "none";
    }
};

function scrollToTitle() {
    const titleSection = document.getElementById("title");
    if (titleSection) {
        const top = titleSection.offsetTop;
        window.scrollTo({
            top: top,
            behavior: "smooth"
        });
    } else {
        console.log("Title section not found.");
    }
}
