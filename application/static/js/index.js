const messageInput = document.getElementById("message-input");
const socketio = io({autoConnect:false});
socketio.connect()

const handleImage = () => {
  const input = document.getElementById('img-input');
  const preview = document.getElementById('prof-img');
  const form = document.getElementById('upload-prof-img');
  // form.submit();
  if (input.files && input.files[0]) {
    // const reader = new FileReader();
    //
    // reader.onload = function (e) {
    //   preview.src = e.target.result;
    // };
    //
    // reader.readAsDataURL(input.files[0]);
    //
    // Submit the form programmatically after selecting the image
    form.submit();
    let pF = document.forms["change-password-form"];
    let nF = document.forms["change-name-form"];
    pF["password1"].value = ""  
    pF["password2"].value = ""  
    pF["password3"].value = ""  
    nF["name"].value = ""  

  }
}

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
  // const handleImage = () => {
  //   const input = document.getElementById('img-input');
  //   const preview = document.getElementById('prof-img');
  //   const form = document.getElementById('upload-prof-img');
  //   form.submit();
    // if (input.files && input.files[0]) {
    //   const reader = new FileReader();
    //
    //   reader.onload = function (e) {
    //     preview.src = e.target.result;
    //   };
    //
    //   reader.readAsDataURL(input.files[0]);
    //
    //   // Submit the form programmatically after selecting the image
    //   form.submit();
    // }
  // }
  // document.getElementById("img-input").addEventListener("onchange",()=>{
  //   handleImage()
  //   console.log("imga")
  // })
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

const EnterChatRoom = (chatsSection,chatRoomSection)=>{
  let roomBtns = document.getElementsByClassName("enter");
  for (let roomBtn of roomBtns){
    roomBtn.addEventListener("click",()=>{
      socketio.emit("join",{room : roomBtn.value})
      document.getElementById("room-title").innerText = roomBtn.value
      socketio.on("get_room_messages",(roomMsgs)=>{
        chatsSection.style.display = "none";
        chatRoomSection.style.display = "block";
        console.log(roomMsgs)
      })
    })
  }
}

const ExitChatRoom = (chatsSection,chatRoomSection)=>{
  document.getElementById("exit-room").addEventListener("click",()=>{
    chatsSection.style.display = "block";
    chatRoomSection.style.display = "none";
    // document.getElementById("messages").innerHTML = " ";
  })
}

const sendMessage = (msgInput,room,sender_id) =>{
 socketio.emit("message",{message : msgInput.value,room : room ,sender_id: sender_id});
  msgInput.value = "";

}

const displayMessage = (messageDiv,msgContainer,message,time,direction,sender_img=null)=>{
  if (message){
    if (direction == "right"){
      messageDiv.setAttribute("class",`card align-self-end mb-3 pb-0 ml-0`);
      messageDiv.innerHTML = `
      <div class="card-body pb-0">
        <p class="card-text mb-0 pb-0">${message}</p>
        <p class="card-text m-0 p-0" style="text-align: right;"><small class="text-body-secondary">${time}</small></p>
      </div>
      `;
      msgContainer.appendChild(messageDiv);
      console.log("append the message");
    }
    else{
      messageDiv.setAttribute("class","card mb-3 pb-0 ml-0");
      messageDiv.innerHTML = `
      <div class="card-header d-flex">
        <img src="data:image/png;base64,${sender_img}" class="card-img-top align-self-start" alt="..." style="width:30px;height:30px;border-radius:50%;">
        <span class="m-15">kibuule_noah</span>
      </div>
      <div class="card-body pb-0">
        <p class="card-text mb-0 pb-0">${message}</p>
        <p class="card-text m-0 p-0" style="text-align: right;"><small class="text-body-secondary">${time}</small></p>

      </div>
      `;
      msgContainer.appendChild(messageDiv);
      console.log("append the message");
    }
  }
}

const yourRoom = (name,moto,photo=null)=>{
  return `
    <img style="height:3rem;width:3rem;" class="h-img align-self-center pb-0 mb-0" src="{{url_for('static',filename='imgs/image.jpg')}}" class="card-img-top" alt="..."> 
    <div class="card-body d-flex flex-column mt-0 pt-0"> 
      <p class="card-title sm-card-title align-self-center">${name}<sup style="color:green;">*new</sup></p> 
      <p class="card-text">moto: ${moto}</p> 
      <button class="btn btn-primary align-self-center sm-btn pb-0 pt-0 mb-0 mt-0 enter" value=${name}>Enter</button> 
   </div> `
}


const createYourRoomCard = (roomName,roomMoto)=>{
  let yourRoomsSection = document.getElementById("your-rooms");
  let test = document.createElement("div");
  test.setAttribute("class","card d-flex pt-0 pb-0 room-card")
  test.style.border = "1px solid green"
  test.innerHTML = yourRoom(roomName,roomMoto);
  yourRoomsSection.appendChild(test);

};

const clearForm = (form)=>{
  form["room-name"].value = "";
  form["room-moto"].value = "";
  form["room-image"].value = "";

}

if (document.title == "dashboard"){
  let chatsSection = document.getElementById("chats-display");
  let chatRoomSection = document.getElementById("chat-room");
  
  // const EnterChatRoom = (value,chatsSection=chatsSection,chatRoomSection=chatRoomSection)=>{
  //     socketio.emit("join",{room : roomBtn.value})
  //     document.getElementById("room-title").innerText = value
  //     socketio.on("get_room_messages",(roomMsgs)=>{
  //       chatsSection.style.display = "none";
  //       chatRoomSection.style.display = "block";
  //       console.log(roomMsgs)
  //     })
  //   }
  // }

  let createRoomBtn = document.getElementById("create-btn");
  let createRoomToastElement = document.getElementById("create-room-toast");


  let createRoomToast = new bootstrap.Toast(createRoomToastElement);
  createRoomBtn.addEventListener("click",()=>createRoomToast.show());

  var userId = 0 
  var room = ""  
  
  document.getElementById("create-room-btn").addEventListener("click",()=>{
    let form = document.forms["create-room-form"];

    let roomName = form["room-name"].value//.value)
    let roomMoto = form["room-moto"].value
    let roomImage = form["room-image"].value
    if (roomName && roomMoto){
      socketio.emit("create_room",{name:roomName,moto: roomMoto,image:roomImage});
      socketio.on("confirm_room_exists",(res)=>{
        console.log(res)
        console.log(typeof res)
        if (!res){
          createYourRoomCard(roomName,roomMoto);
          clearForm(form);
          createRoomToast.hide();
        }
        else{
          clearForm(form);
        }
      })
    }
  })
  
  EnterChatRoom(chatsSection,chatRoomSection);  
  ExitChatRoom(chatsSection,chatRoomSection);  

  let msgContainer = document.getElementById("messages")
  let msgInput = document.getElementById("message-input");
  let sendBtn = document.getElementById("send-btn")
  
  socketio.on("send_ids",(idObj)=>{
    userId = idObj.user_id 
    room = idObj.room

    sendBtn.addEventListener("click",()=>{
      sendMessage(msgInput,room,userId);
      
      document.getElementById("bottompage").scrollIntoView();
    })
    const giveMessageDirection = (id1,id2) => id1 === id2 ? "right" : "left"

    socketio.on("message",(msgObj)=>{
      let messageDiv1 = document.createElement("div");
      let message = msgObj.message;
      let time = msgObj.time;
      let direction = giveMessageDirection(msgObj.id,userId);

      displayMessage(messageDiv1,msgContainer,message,time,direction);
      
    })
    socketio.on("get_room_messages",(roomMsgs)=>{
      for (let msgobj of roomMsgs){
        let messageDiv2 = document.createElement("div");
        let sender_id = msgobj[1];
        let msg = msgobj[2];
        console.log(msgobj[0])
        let time = "coming";
        let direction = giveMessageDirection(sender_id,userId);

        displayMessage(messageDiv2,msgContainer,msg,time,direction,sender_id=msgobj[0]);
      }
    })
  })
}
// <button type="button" class="btn btn-secondary" data-bs-toggle="tooltip" data-bs-placement="bottom" data-bs-title="Tooltip on bottom">
  // Tooltip on bottom
// </button>
