console.log("Hello World")
function updateMapImageTimer() {
    delay = window.setTimeout(updateMapImage, 5000)     //calls function to refresh web page after 5 seconds to update map. Not the cleanest way of doing so, refreshing just the image would be better, but thats almost the entire web page anyway so meh :shrug:
}
function updateMapImage() {
    location.reload()  
}

updateMapImageTimer()