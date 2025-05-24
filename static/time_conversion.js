function getLang() {
    // credit to Fiach Reid for writing this
    if (navigator.languages !== undefined) 
        return navigator.languages[0]; 
    return navigator.language;
}

const dayOfWeekTranslator = new Intl.DateTimeFormat(getLang(), {'weekday':'long'});

function humanTime(secondsThen) {
    const time = new Date(secondsThen*1000);
    const secondsNow = Date.now() / 1000;
    //console.log(`msg at ${secondsAgo} seconds ago`);
    const minutesAgo = (secondsNow - secondsThen)/60;
    if (minutesAgo < 0) return "In the future somwhere...";
    if (minutesAgo < 2) return "Just now";
    if (minutesAgo < 72)
        return Math.round(minutesAgo).toString() + " minutes ago";
    if (minutesAgo < 60*24)
        return Math.round(minutesAgo/60).toString() + " hours ago";
    if (minutesAgo < 24*60*6)
        return dayOfWeekTranslator.format(time) + ' at ' + time.getHours()+':'+time.getMinutes();
    if (minutesAgo < 24*60*365)
        return (minutesAgo/(24*60)).toString() + " days ago"
    return time.toString();
}