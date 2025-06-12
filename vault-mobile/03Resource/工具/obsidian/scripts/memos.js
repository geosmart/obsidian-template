
module.exports = start;


async function start(apiUrl,openId,offset=0,limit=20,limit_days=2) {
    const results= await getMemos(apiUrl,openId,offset,limit);
    
    var res=""
    results.data.forEach(item => {
        const days=getDaysDifference(item.createdTs,Date.now()/1000)
        if (days<=limit_days){
            time=unixTimestampToDateTime(item.createdTs)
            res+=`## @${time}\n${item.content}\n`;   
        } 
    })

    return res
}


async function getMemos(apiUrl,openId,offset,limit) {
    return apiGet(`${apiUrl}`, {
        openId: openId,
        rowStatus: "NORMAL",
        offset: offset,
        limit:limit
    });
}

async function apiGet(url, data) {
    let finalURL = new URL(url);
    Object.keys(data).forEach(key => finalURL.searchParams.append(key, data[key]));
    
    return await fetch(finalURL, {
        method: 'GET', cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(async (res) => await res.json());
}

function getDaysDifference(timestamp1, timestamp2) {
    var milliseconds1 = timestamp1 * 1000;
    var milliseconds2 = timestamp2 * 1000;
  
    var difference = Math.abs(milliseconds1 - milliseconds2);
  
    var days = Math.floor(difference / 86400000);
  
    return days;
  }
  

function unixTimestampToDateTime(unixTimestamp) {
    var date = new Date(unixTimestamp * 1000);
  
    var year = date.getFullYear();
    var month = ("0" + (date.getMonth() + 1)).slice(-2);
    var day = ("0" + date.getDate()).slice(-2);
    var hours = ("0" + date.getHours()).slice(-2);
    var minutes = ("0" + date.getMinutes()).slice(-2);
    return year + "-" + month + "-" + day + " " + hours + ":" + minutes;
}

// await start(2)