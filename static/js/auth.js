const Signup = async () =>{
    
    try { 
        const Details = {}
        Details.firstname = document.getElementById("firstname").value
        Details.email = document.getElementById("email").value
        Details.lastname = document.getElementById("lastname").value
        Details.password = document.getElementById("password").value
      
        console.log("details",Details);
        // var spin = document.getElementById("spin")
        // spin.style.display = "block"


        const resp = await  axios.post('/signup', Details,{
            headers:{
                'Content-Type': 'application/json'
            }
            
        });
        
        //  console.log(resp.data);
        if (resp.data.status==200) {
            // var notify = document.getElementById("notification")
            // document.getElementById('alertmsg').innerText = resp.data.msg
            // notify.style.display = "block"
            // spin.style.display = "none"
            window.location.replace("/dashboard")
            console.log(resp);
        }

        if(resp.data.status==404){
            var notify = document.getElementById("notification")
            //  document.getElementById("alertmsg").innerText = resp.data.msg
            // notify.classList.remove("is-primary")
            // notify.classList.add("is-danger")
            // notify.style.display = "block"
            // spin.style.display = "none"
        }

    } catch (error) {
      console.log(error.response.data);
    }


  }


  const Signin = async () =>{

    try { 
        const Details = {}
        Details.email = document.getElementById("email").value
        Details.password = document.getElementById("password").value
        // var spin = document.getElementById("spin")
        // arrow.style.display = "none"
        // spin.style.display = "block"


        const resp = await  axios.post('/signin', Details,{
            headers:{
                'Content-Type': 'application/json'
            }
            
        });
        
        // console.log(resp.data);
        if (resp.data.status==200) {
            var notify = document.getElementById("notification")
            // document.getElementById('alertmsg').innerText = resp.data.msg
            // notify.style.display = "block"
            // spin.style.display = "none"
            // console.log(resp);
            window.location.replace("/dashboard")
        }

        if(resp.data.status==404){
            var notify = document.getElementById("notification")
            // document.getElementById("alertmsg").innerText = resp.data.msg
            // notify.classList.remove("is-primary")
            // notify.classList.add("is-danger")
            // notify.style.display = "block"
            // spin.style.display = "none"
        }

    } catch (error) {
      console.log(error)
    }


  }

