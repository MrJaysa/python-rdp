var server_link;
var attempt = false
var discont = false;
var socket;
var con_user;
var setEnlarge = true;

new QWebChannel(qt.webChannelTransport, function (channel){
    window.handler = channel.objects.handler;

    handler.uiSignal.connect((contents) => {
        devs_list.innerHTML = contents;
        
        document.querySelectorAll(".connect_form").forEach(form => {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                form_loader.style.display = "block";
                socket.emit('connect_users', {
                    id:  form['rid'].value,
                    pwd: form['pwd'].value
                });

                socket.on('establish_connection', (msg)=> {
                    if (msg.status == 200){
                        palert_body.style.display = 'none';
                        con_form.style.display = "none";
                        devs_list.style.display = 'none'
                        err_msg.style.display = "none"
                        discon.style.display = "none"
                        form.getElementsByClassName('form-err')[0].style.display = 'none';
                        con_user = msg.user;

                        socket.emit('trigger_desktop', con_user)
                        
                        socket.on('img_stream', (data)=> {
                            main.style.display = 'none !important';
                            main.classList.add('d-none');
                            main.classList.remove('d-flex');
                            stream.style.display = 'block !important';
                            stream.classList.remove('d-none');
                            stream.classList.add('d-flex');
                            stream_img.src = data;
                            if (setEnlarge){
                                handler.start_stream()
                                setEnlarge = false
                            }
                            socket.emit('received_signal', con_user)
                        })
                        
                    } else {
                        form.getElementsByClassName('form-err')[0].style.display = 'block'
                    }
                    form_loader.style.display = "none"
                })
            })

            // start loader
            // verify password data
            // change interface
            // present error message on that place
        })
    });
    // handler.init()
})
            
palert_close.addEventListener('click', ()=>{
    palert_body.style.display = 'none';
    loader.style.display = "none"
    palert_img.innerHTML = `<img height="100px" src="./images/refresh.gif" alt="loading">`;
    palert_msg.innerText = "Please wait, your request is been processed.";
    con_form.style.display = "block"
    devs_list.style.display = 'none'
})

// button triggered
conbtn.addEventListener('click', ()=>{
    palert_body.style.display = 'flex';
    err_msg.style.display = "none";
    discon.style.display = "none";
});
// handler.init()
rebtn.addEventListener('click', ()=>{
    socket.reconnect();
});

con_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    server_link = con_form['servername'].value;
    con_form.style.display = "none";

    loader.style.display = "block"
    socket = io.connect(server_link);

    socket.on('connect_error', () => {
        if (attempt) {
            let timout = setTimeout(()=>{
                socket.disconnect()
            }, 120000);
            err_r.style.display = "block"
            rebtn.style.display = "block";
            clearTimeout(timout);
        } else {
            socket.disconnect();
        }
        err_msg.style.display = "block";
        loader.style.display = "none";
        conbtn.style.display = "block";
        disbtn.style.display = "none";
        err_r.style.display = "none"
        discon.style.display = "none";
        devs.style.display = "none";
    })
    
    socket.on('disconnect', () => {
        if (discont == false){
            palert_body.style.display = 'flex';
            discon.style.display = "block";
            err_msg.style.display = "none";
            con_form.style.display ="none";
            loader.style.display ="none";
        }
        discont = false;
        setEnlarge = true;
    })
    
    socket.on('connect', () => {
        socket.send({
            id: con_form['id'].value,
            type: 'client',
        });
        attempt = true;
        rebtn.style.display = "none";
        // palert_body.style.display ="none";
    });
    
    socket.on('message', (msg) => {
        if (msg.status_id == con_form['id'].value) {
            palert_img.innerHTML = '<i class="ri ri-checkbox-circle-fill text-green" style="font-size: 150px;"></i>';
            palert_msg.innerText = "Your request has been processed, and it was successful!. \n You have been connected successfully to the Remote desktop local server. \n A client whom you have shared your details with will soon connect to you shortly";
            conbtn.style.display = "none";
            disbtn.style.display = "block";
            devs.style.display = "block";
            handler.save_devices(msg.user)
        } else {
            handler.save_devices(msg.user)
        }
    })
});

disbtn.addEventListener('click', ()=> {
    discont = true;
    socket.disconnect();
    conbtn.style.display = "block";
    disbtn.style.display = "none";
    err_r.style.display = "none"
    discon.style.display = "none";
    devs.style.display = "none";
})

devs.addEventListener('click', ()=> {
    handler.load_devs()
    palert_body.style.display = 'flex';
    con_form.style.display = "none";
    devs_list.style.display = 'block'
    err_msg.style.display = "none"
    discon.style.display = "none"
})

stream_img.addEventListener('mousedown', (e) => {
    if (e.which == 3){
        console.error('right click')
    } 
    if (e.which == 1){
        console.error('left click')
    } 
})

stream_img.addEventListener('mousemove', (e) => {
    console.error(e.offsetX, e.offsetY)
})

stream_img.addEventListener("keypress", (e) => {
    console.error(e.key)
});

// class Test {
//     constructor(...classes) {
//         this.classes = classes;
//     }

//     // this method is a test
//     spring() {
//         return this.sides;
//     }

//     view() {
//         // loop all classes, hide views not needed
//     }

//     close_modal() {
//         // reset the view
//     }

//     open_modal() {
//         // open modal to the current view required
//     }
// }