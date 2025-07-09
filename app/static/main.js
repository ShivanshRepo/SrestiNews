// 📁 static/main.js

// Confirm before deleting news
document.addEventListener("DOMContentLoaded", function () {
  const deleteButtons = document.querySelectorAll(".btn-danger");

  deleteButtons.forEach(button => {
    button.addEventListener("click", function (event) {
      const confirmDelete = confirm("Are you sure you want to delete this news item?");
      if (!confirmDelete) {
        event.preventDefault(); // stop deletion
      }
    });
  });
});

// Optional: Auto-hide flash messages after 3 seconds
setTimeout(() => {
  const alertBox = document.querySelector(".alert");
  if (alertBox) {
    alertBox.style.display = "none";
  }
}, 3000);
// In static/main.js
function previewImage(input) {
  const preview = document.getElementById("preview");
  const file = input.files[0];
  const reader = new FileReader();
  reader.onload = function (e) {
    preview.src = e.target.result;
    preview.classList.remove("d-none");
  };
  reader.readAsDataURL(file);
}
