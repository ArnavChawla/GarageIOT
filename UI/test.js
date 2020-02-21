const netList = require('network-list');


netList.scan({}, (err, arr) => {
    arr.forEach(element => {
        if(element.hostname == "dex.lan")
        {
            console.log(element.ip)
        }
    });
});

