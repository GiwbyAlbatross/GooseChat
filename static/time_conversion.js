function getLang() {
    // credit to Fiach Reid for writing this
    if (navigator.languages !== undefined) 
        return navigator.languages[0]; 
    return navigator.language;
}

const dayOfWeekTranslator = new Intl.DateTimeFormat(getLang(), {'weekday':'long'});

function humanTime(seconds) {
    const time = new Date(seconds*1000);
    const minutesAgo = ((Date.now().getTime() / 1000) - seconds)/60;
    if (minutesAgo < 16)
        return minutesAgo.toString() + " minutes ago";
    if (minutesAgo < 24*60*6)
        return dayOfWeekTranslator.format(time) + ' at ' + time.getHours()+':'+time.getMinutes();
    if (minutesAgo < 24*60*365)
        return (minutesAgo/(24*60)).toString() + " days ago"
    return time.toString();
}