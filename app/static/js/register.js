function messRegister(username,firstname,lastname,password,comfirm){
            fetch('/api/register', {
                method: "post",
                body: JSON.stringify({
                    "username":username,
                    "firstname":firstname,
                    "lastname":lastname,
                    "password":password,
                    "comfirm":comfirm
                }),
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(res => res.json()).then(data => {
                console.info(data)
                if(data.mess == "thanh cong"){
                    window.location.href='/register/avatar'
                }else{
                    alert('username đã tồn tại')
                }
            }) // js promise
        }