setInterval(myWatch, 100)

function myWatch(){
    let date = new Date()
    let now = date.toLocaleTimeString()
    document.getElementById('demo').innerHTML = now;
}