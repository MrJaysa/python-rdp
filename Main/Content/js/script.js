var server_link;
var socket;
var con_user;

new QWebChannel(qt.webChannelTransport, function (channel){
    window.handler = channel.objects.handler;

    handler.customSignal.connect(function(img) {
        socket.emit("streamer", {
            data: img,
            user: con_user
        })
    });
})
            
palert_close.addEventListener('click', ()=>{
    palert_body.style.display = 'none';
    palert_img.innerHTML = `<img height="100px" src="./images/refresh.gif" alt="loading">`;
    palert_msg.innerText = "Please wait, your request is been processed.";
    loader.style.display = "none"
    net_form.style.display = "none"
    con_form.style.display = "block"
})

// button triggered
conbtn.addEventListener('click', ()=>{
    palert_body.style.display = 'flex';
});

con_form.addEventListener('submit', (e) => {
    e.preventDefault();
    server_link = con_form['servername'].value;
    con_form.style.display = "none";
    net_form.style.display = "block"
})

net_form.addEventListener('submit', async(e) => {
    e.preventDefault();
    formData = new FormData(net_form);

    net_form.style.display = "none"
    loader.style.display = "block"
    
    socket = io.connect(server_link);

    socket.on('connect', () => {
        socket.send({
            id: rdp_id.value,
            pass: rdp_password.value,
            type: 'desktop'
        });
    });

    socket.on('connect_error', () => {
        loader.style.display = "none"
        con_form.style.display = "block";
        err_msg.style.display = "block";
        server_value = server_link;
        net_form.style.display = "none";
    })

    socket.on('message', (msg) => {
        if (msg.status == 200) {
            palert_img.innerHTML = '<i class="ri ri-checkbox-circle-fill text-green" style="font-size: 150px;"></i>';
            palert_msg.innerText = "Your request has been processed, and it was successful!. \n You have been connected successfully to the Remote desktop local server. \n A client whom you have shared your details with will soon connect to you shortly";
            conbtn.style.display = "none";
            disbtn.style.display = "block";
        } else {
            palert_img.innerHTML = '<i class="ri ri-close-circle-fill text-danger" style="font-size: 150px;"></i>';
            palert_msg.innerText = "Your request failed!.";
        }
    })
    
    socket.on('establish_connection', (msg)=> {
        if (msg.status == 200){
            con_user = msg.user;
            handler.init()
        } else {
            console.error("unable to establish connection.")
        }
    })
    // socket.on('disconnect', () => {
    //     if (discont == false){
    //         palert_body.style.display = 'flex';
    //         discon.style.display = "block";
    //         err_msg.style.display = "none";
    //         con_form.style.display ="none";
    //         loader.style.display ="none";
    //     }
    //     discont = false
    // })
});


disbtn.addEventListener('click', ()=> {
    discont = true;
    socket.disconnect();
    handler.terminate_stream()
    conbtn.style.display = "block";
    disbtn.style.display = "none";
})