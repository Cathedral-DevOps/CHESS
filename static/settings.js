

const Confirm = document.getElementById("confirm");
const Deny = document.getElementById("deny");
let CurrentSetting = ""


Confirm.addEventListener("click", function () 
{
CurrentSetting = "ChessMax"
localStorage.setItem("settings", CurrentSetting);
});
// No chess max :(
Deny.addEventListener("click", function () 
{
    CurrentSetting = "NoChessMax"
    localStorage.setItem("settings", CurrentSetting);
});