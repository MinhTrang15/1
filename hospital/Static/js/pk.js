function create(id, name) {
    fetch('/api/create', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        window.location.href ="/don-thuoc"
    })
}

function add_thuoc(name,sl) {
    fetch('/api/add-thuoc', {
        method: "post",
        body: JSON.stringify({
            "name": name,
            "sl" : sl
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
    })
}