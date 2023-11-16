let messageInput = document.getElementById("message-input");
var userId = 0 
var room = ""

const socketio = io({autoConnect:false});
socketio.connect()

const startsWithdigit = (str)=>/^[0-9].+/.test(str);
const validatePasswordFormat = (pwd)=>/^(?=(.*\d){2,})(?=(.*[a-z]){3,})(?=(.*[A-Z]){1,})(?=(.*\W){1,}).{6,12}$/.test(pwd);

if (document.title == "profile"){
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
      passwordToast.hide();
    });
    changePasswordBtn.addEventListener("click",()=>{
      passwordToast.show();
      nameToast.hide();
    });
  });
}

if (document.title == "room"){
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
}


const flash = (node,message,position='after')=>{
  var error_node = document.createElement("span");
  error_node.style.color = "red"
  error_node.innerText = `${message}`
  error_node.className = "text-wrap"
  if (node.nextSibling.nodeName != "SPAN"){
    if (position == "after"){
      node.after(error_node);
    }
    else{
      node.before(error_node);
    }
  }
}

const validateCreateForm = () => {
  let form = document.forms["create-form"];
  
  if (form["name"].value.length < 3){
    flash(form["name"],"name is too short");
    return false;
  }
  else if (startsWithdigit(form["name"].value)){
    flash(form["name"],"name can't start with a digit");
    return false
  }
  else if (!validatePasswordFormat(form["password1"].value)){
    flash(form["password1"],"too weak password, should have 2 digits min,3 lower letters(min) 1 upper letter and symbol(min)");
    return false
  }
  else if (form["password1"].value != form["password2"].value){
    flash(form["password2"],"this password doesn't match the first one")
    return false;
  }
  else{
    return true;
  }
}

const validateLoginForm = ()=>{
  let form = document.forms["login-form"];
  
  if (form["name"].value.length < 3){
    flash(form["name"],"invalid name lenth");
    return false;
  }
  else if (!validatePasswordFormat(form["password"].value)){
    flash(form["password"],"invalid password format");
    return false
  }
}

const validateChangeNameForm = ()=>{
  let changNameForm = document.forms["change-name-form"];
  let userName = changNameForm["name"];

  if (userName.value.length == 0){
    flash(userName,"nothing in put, name not changed");//,position="before");
    return false;
  }
  else if(userName.value.length <= 2){
    flash(userName,"new name is too short");
    return false
  }
  else if(startsWithdigit(userName.value)){
    flash(userName," name can't start with a digit")
    return false
  }
  // else{
    // return true;
  // }
}

const validateChangePasswordForm = ()=>{
  let passwordForm = document.forms["change-password-form"];
  if (!validatePasswordFormat(passwordForm["password2"].value)){
    flash(passwordForm["password2"],"too weak password, it should have 2 digits min,3 lower letters(min) 1 upper letter and symbol(min)");
    return false;
  }
  else if (passwordForm["password2"].value != passwordForm["password3"].value){
    flash(passwordForm["password3"],"this password doesn't match the first one");
    return false;
  }
}

if (document.title == "create" || document.title == "login" || document.title == "profile"){
  let inputs = document.getElementsByTagName("input");
  for (let inp of inputs){
    inp.addEventListener("input",()=>{      
      if (inp.nextSibling.nodeName == "SPAN"){
        inp.nextSibling.remove()
      }
    })
  }
}

if (document.title == "dashboard"){
  alert("dashboard")
  fBtn = document.getElementById("f")
  fBtn.addEventListener("click",()=>{
    socketio.emit("user_join_one",fBtn.value)
    // window.location.href = "/vws/oneonone"
  //   socketio.on("send_ids",(idObj)=>{
  // 
  //     userId = idObj.user_id 
  //     room = idObj.room
  //     // console.log(userId,room) 
  //   })
    window.location.href = "/vws/oneonone"
    // socketio.emit("user_join_one",{room:fBtn.value})
  })
  // var userId = 0 
  // var room = null;
  
}

if (document.title == "one-on-one"){
  socketio.emit("reach","k");
  // var userId = null
  // var userSid = null
  let msgContainerOne = document.getElementById("messages-one")
  let msgInputOne = document.getElementById("msginput-one");
  let sendBtnOne = document.getElementById("sendbtn-one")
  
  // socketio.emit("user_join_one")
  // socketio.on("send_ids",(id)=>{
  //   userId = id;
  //   alert(id);
  //     
  //   // userSid = idObj.sid; 
  // })
  socketio.on("send_ids",(idObj)=>{
    userId = idObj.user_id 
    room = idObj.room
    // alert(userId,room)
  })

  sendBtnOne.addEventListener("click",()=>{
    socketio.emit("message-one",{"message" : msgInputOne.value,"room" : room });
    msgInputOne.value = "";
    document.getElementById("bottompage").scrollIntoView();
  })
  const giveMessageDirection = (id1,id2) => id1 === id2 ? "end" : "start"

  socketio.on("message-one",(msgObj)=>{
    message = document.createElement("div");
    let direction = giveMessageDirection(msgObj.id,userId)

    message.setAttribute("class",`card align-self-${direction} mb-3 pb-0 ml-0`);
    message.innerHTML = `
    <div class="card-body pb-0">${msgObj.id} ${direction}
      <p class="card-text mb-0 pb-0">${msgObj.message}</p>
      <p class="card-text m-0 p-0" style="text-align: right;"><small class="text-body-secondary">${msgObj.time}</small></p>
    </div>
    `;
    msgContainerOne.appendChild(message);
  })
}
