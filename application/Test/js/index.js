let messageInput = document.getElementById("message-input");

document.addEventListener("DOMContentLoaded", function(){
  var changeNameBtn = document.getElementById("change-name-btn");
  var changePasswordBtn = document.getElementById("change-password-btn");
  var changeNameElement = document.getElementById("change-name");
  var changePasswordElement = document.getElementById("change-password");

  // Create toast instance
  var nameToast = new bootstrap.Toast(changeNameElement);
  var passwordToast = new bootstrap.Toast(changePasswordElement);

  changeNameBtn.addEventListener("click", ()=>{
    nameToast.show();
  });
  changePasswordBtn.addEventListener("click",()=>{
    passwordToast.show();
  });
});

  // Custom JavaScript to expand the text area
messageInput.addEventListener("input", (e)=>{
    if (e.target && e.target.nodeName === "TEXTAREA") {
        autoExpand(e.target);
    }
});

function autoExpand(textarea) {
    // textarea.style.height = "10px";
    textarea.style.height = (textarea.scrollHeight) + "px";
    textarea.style.maxHeight = "100px"
};
