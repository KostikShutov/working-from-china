class ConfigUrls:
    TELEGRAM_URL = "https://core.telegram.org/resources/cidr.txt"
    WHATSAPP_URL = "https://raw.githubusercontent.com/HybridNetworks/whatsapp-cidr/refs/heads/main/WhatsApp/whatsapp_cidr_ipv4.txt"
    META_URL = "https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/meta.lst"
    META_URL_OPEN = "https://iplist.opencck.org/?format=text&data=cidr4&site=messenger.com&site=whatsapp.com&site=instagram.com&site=facebook.com"
    YOUTUBE_URL = "https://raw.githubusercontent.com/touhidurrr/iplist-youtube/refs/heads/main/lists/cidr4.txt"
    YOUTUBE_URL_OPEN = "https://iplist.opencck.org/?format=text&data=cidr4&site=youtube.com"
    OTHERS_URL = "https://gist.githubusercontent.com/iamwildtuna/7772b7c84a11bf6e1385f23096a73a15/raw/9aa7c097b0721bac547fa26eb2cbf6c58d3cf22b/gistfile2.txt"
    JETBRAINS_URL_OPEN = "https://iplist.opencck.org/?format=text&data=cidr4&site=jetbrains.com&site=jetbrains%40cdn&site=jetbrains%40grazie.ai"
    JETBRAINS_URL_OWN = "https://raw.githubusercontent.com/KostikShutov/iplist-jetbrains/refs/heads/main/lists/cidr4.txt"
    TWITTER_URL_OPEN = "https://iplist.opencck.org/?format=text&data=cidr4&site=x.com"
    CHATGPT_URL_OPEN = "https://iplist.opencck.org/?format=text&data=cidr4&site=chatgpt.com"
    MEDIUM_URL_OPEN = "https://iplist.opencck.org/?format=text&data=cidr4&site=medium.com"
    LINKEDIN_URL_OPEN = "https://iplist.opencck.org/?format=text&data=cidr4&site=linkedin.com"


class ConfigNames:
    CHATGPT = "chatgpt"
    JETBRAINS = "jetbrains"
    LINKEDIN = "linkedin"
    MEDIUM = "medium_com"
    META = "meta"
    TELEGRAM = "telegram"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    OTHERS_LIST = [CHATGPT, LINKEDIN, MEDIUM, META, TWITTER, YOUTUBE]
