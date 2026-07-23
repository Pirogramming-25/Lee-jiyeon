function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(";") : [];
    for (const c of cookies) {
        const cookie = c.trim();
        if (cookie.startsWith(`${name}=`)) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return null;
}