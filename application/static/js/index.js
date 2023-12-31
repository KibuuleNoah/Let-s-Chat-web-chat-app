const messageInput = document.getElementById("message-input");
const socketio = io({autoConnect:false});
socketio.connect()

const truct_text = (text)=>{
  return text.length > 10 ? text.slice(0,10)+"..." : text
}

//send the cropped image to the backend
const sendToFlaskBackend = (croppedDataURL,endpoint)=> {
  // Make an HTTP POST request to your Flask backend
  fetch(`http://127.0.0.1:5000${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ imageData: croppedDataURL }),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Response from Flask:', data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

//read an image from input and crops it then it can
//send it via the fetch or socketio
const cropAndSendImage = (input,endpoint=null,socket=null,args=null)=> {
  const file = input.files[0];
  // Check if a file is selected
  if (file) {
    const reader = new FileReader();
    // Read the file as a data URL
    reader.readAsDataURL(file);
    reader.onload = function (e) {
      // Create an image element
      const img = new Image();
      img.src = e.target.result;
      // Set up an event listener for the image load
      img.onload = function () {
        // Create a canvas element
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        // Set the canvas dimensions to 200x200
        canvas.width = 200;
        canvas.height = 200;
        // Draw the image on the canvas with 200x200 dimensions
        ctx.drawImage(img, 0, 0, 200, 200);
        // Get the cropped image as a data URL
        const croppedDataURL = canvas.toDataURL('image/png');
        // console.log(croppedDataURL);
        if (endpoint && !socket){
          sendToFlaskBackend(croppedDataURL,endpoint);
          window.location.href = "/vws/";
        }
        else if (socket && !endpoint){
          socketio.emit(socket,{"imageData":croppedDataURL,args:args});
        }
      };
    };
  }
}

const submitRoomUpdates = ()=>{
  let input = document.getElementById("room-image");
  cropAndSendImage(input,window.location.pathname);
  document.getElementById("update-room-form").submit()
      
  window.location.href = "/vws/";
}

//first hold the selected profile image 
//and first crops it then submit it
const changeProfileImage = () => {
  const input = document.getElementById('img-input');
  const preview = document.getElementById('prof-img');
  const form = document.getElementById('upload-prof-img');
  
  cropAndSendImage(input,"/vws/profile",null);
  input.value = ""; 
  // if (input.files && input.files[0]) {
    // Submit the form programmatically after selecting the image
    // form.submit();
    // let pF = document.forms["change-password-form"];
    // let nF = document.forms["change-name-form"];
    // pF["password1"].value = ""  
    // pF["password2"].value = ""  
    // pF["password3"].value = ""  
    // nF["name"].value = ""  
  // }
}

//(regex) checkes if a str starts with a digit e.g in name
const startsWithdigit = (str)=>/^[0-9].+/.test(str);
//this validates a password if it follows a give rule;
//atleast 2 digits, 3 lower case letters, 1 upper case letter, atleast 1 symbol
//and min length of 7 and max of 12
const validatePasswordFormat = (pwd)=>/^(?=(.*\d){2,})(?=(.*[a-z]){3,})(?=(.*[A-Z]){1,})(?=(.*\W){1,}).{7,12}$/.test(pwd);

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



//used to display error and success message to data input form
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

//validates if create form input data is in corrent format before submitting
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

//validates if login input data is in corrent format before
//even checking if the user exists
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

//validates change name form in profile before submittion
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
//validates change password form in profile before submittion
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

//enters the user into the room
const EnterChatRoom = (chatsSection,chatRoomSection)=>{
  let roomBtns = document.getElementsByClassName("enter");
  for (let roomBtn of roomBtns){
    let roomName = roomBtn.value;
    roomBtn.addEventListener("click",async ()=>{
      socketio.emit("join",{room : roomName})
      let roomTitle = document.getElementById("room-title");
      roomTitle.innerText = roomName; 
      if (roomName.length < 10){
        roomTitle.style.animation = "none"
        roomTitle.style.transform = "none"
      }
      //loads room image into the chat room nav bar
      await fetch("http://127.0.0.1:5000/GRI",{
        method:"POST",
        headers:{
          "Content-Type":"application/json"
        },
        body:JSON.stringify({roomName:roomName})
      })
        .then( async res => {
          data = await res.json();
          document.getElementById("room-nav-img").src = "data:image/png;base64, "+data["imageData"];
        })

      // console.log("SIB-:",roomBtn.previousSibling.previousSibling);
      socketio.on("get_room_messages",(roomMsgs)=>{
        chatsSection.style.display = "none";
        chatRoomSection.style.display = "block";
        // console.log(roomMsgs)
      })
    })
  }
}

//gets the user out of the room
const ExitChatRoom = (chatsSection,chatRoomSection)=>{
  document.getElementById("exit-room").addEventListener("click",()=>{
    // chatsSection.style.display = "block";
    // chatRoomSection.style.display = "none";
    window.location.href = "/vws/"
  })
}
//sends the message to the backend to be saved and clears message input box
const sendMessage = (msgInput,room,sender_id) =>{
 socketio.emit("message",{message : msgInput.value,room : room ,sender_id: sender_id});
  msgInput.value = "";

}

//displays messages in the room
const displayMessage = (messageDiv,msgContainer,message,time,direction,name,photo)=>{
  if (message){
    // let sender_info = getMsgSenderInfo(sender_id);
    if (direction == "right"){
      messageDiv.setAttribute("class",`card align-self-end mb-3 pb-0 ml-0`);
      messageDiv.innerHTML = `
      <div class="card-body pb-0">
        <p class="card-text mb-0 pb-0">${message}</p>
        <p class="card-text m-0 p-0" style="text-align: right;"><small class="text-body-secondary">utc ${time}</small></p>
      </div>
      `;
      msgContainer.appendChild(messageDiv);
    }
    else{
      messageDiv.setAttribute("class","card mb-3 pb-0 ml-0");
      messageDiv.innerHTML = `
      <div class="card-header d-flex flex-column shrink-1">
        <img src="data:image/png;base64,${photo}" class="card-img-top align-self-start" alt="..." style="width:32px;height:30px;border-radius:50%;">
        <small class="m-15 align-self-end">${name.replace(/\s+/g,"_")}</small>
      </div>
      <div class="card-body pb-0">
        <p class="card-text mb-0 pb-0">${message}</p>
        <p class="card-text m-0 p-0" style="text-align: right;"><small class="text-body-secondary">utc ${time}</small></p>

      </div>
      `;
      msgContainer.appendChild(messageDiv);
      console.log("append the message");
    }
  }
}

const clearForm = (form)=>{
  form["room-name"].value = "";
  form["room-moto"].value = "";
  form["room-image"].value = "";

}

if (document.title == "dashboard"){
  let chatsSection = document.getElementById("chats-display");
  let chatRoomSection = document.getElementById("chat-room");
  
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
    let roomImageInput = form["room-image"]
    if (roomName && roomMoto){
      socketio.emit("create_room",{name:roomName,moto: roomMoto});
      cropAndSendImage(roomImageInput,null,"bounce-save",[roomName])
      socketio.on("confirm_room_exists",(res)=>{
        console.log(res)
        console.log(typeof res)
        if (!res){
          socketio.on("room_img",(imgObj)=>{
            console.log(imgObj)
            window.location.href = "/vws/";
            console.log("created")
            clearForm(form);
            createRoomToast.hide();
          })
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

      displayMessage(messageDiv1,msgContainer,message,time,direction,"boah","data",);

    })
    socketio.on("get_room_messages",(roomMsgs)=>{
      roomMsgs.forEach(msgobj => {
        console.log(msgobj);
        let messageDiv = document.createElement("div");
        let sender_id = msgobj[1]
        let name = msgobj[2];
        let photo = msgobj[3];
        let msg = msgobj[4];
        let time = msgobj[5];
        console.log(name)
        console.log(photo)
        let direction = giveMessageDirection(sender_id,userId);
        console.log(msg,direction,userId)
        
        // let sender_info = getMsgSenderInfo(sender_id);
        // if (sender_info){
          displayMessage(messageDiv,msgContainer,msg,time,direction,name,photo)
      });
    })
  })
  let deletRoomBtns = document.querySelectorAll(".dropdown-item.text-danger");
  for (let deletRoomBtn of deletRoomBtns){
    deletRoomBtn.addEventListener("click",()=>{
      console.log(deletRoomBtn.value) 
      console.log(deletRoomBtn.className)
    })
  }
}
//delete chat room
const deleteRoom = (roomId)=> {
  fetch("/vws/delete-room", {
    method: "POST",
    body: JSON.stringify({ roomId: roomId }),
  }).then((_res) => {
    window.location.href = "/vws/";
  });
}

