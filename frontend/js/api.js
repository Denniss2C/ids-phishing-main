//Para obtener la url de la pestaña actual
async function getCurrentTab() {
    let queryOptions = { active: true, lastFocusedWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

getCurrentTab()
    .then(res => {
        let urlActual = res["url"]
        const json = {
            url: urlActual
        }
        // request options
        const options = {
            method: 'POST',
            body: JSON.stringify(json),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        const image = document.createElement('img');
        image.className="imgResult";
        // send post request
        fetch('https://kevinjair11.pythonanywhere.com/predict', options)
            .then(res => res.json())
            .then(res => {
                let result;
                if (res["result"]==1) {
                    result = "es legítimo";
                    image.src = "../images/Seguro.png";
                }else if (res["result"]==0) {
                    result = "tiene sospechas de phishing";
                } else {
                    result = "tiene phishing";
                    image.src = "../images/Precaución.png";
                }
                document.querySelector(".gif-container").removeChild(document.querySelector(".loading-gif"))
                document.querySelector(".gif-container").removeChild(document.querySelector(".analizando"))    
                document.querySelector(".text-web").innerHTML = "El sitio web "+result;
                document.querySelector('.img-detection').appendChild(image);
                
            })
            .catch(err => console.error(err))
    })
    .catch(err => console.log(err));

