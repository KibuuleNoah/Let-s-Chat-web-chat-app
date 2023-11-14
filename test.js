// let regex = /^(?=(.*\d){2,})(?=(.*[a-z]){3,})(?=(.*[A-Z]){1,})(?=(.*\W){1,}).{6,12}$/;
// let str = "fhF5u76#|#";
// console.log(regex.test(str))
const isdigit = (str)=>/^[0-9].+/.test(str);
let s = "8jjjjgy";
console.log(isdigit(s))
