# https://youtrack.jetbrains.com/articles/SUPPORT-A-288/Whats-the-IP-allowlist-of-IntelliJ-IDE-in-case-of-firewall-policy-or-restricted-network
/ip firewall address-list
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=jetbrains.com
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=download.jetbrains.com
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=download-cf.jetbrains.com
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=download-cdn.jetbrains.com
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=plugins.jetbrains.com
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=account.jetbrains.com
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=cloudconfig.jetbrains.com
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=frameworks.jetbrains.com
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=api.app.prod.grazie.aws.intellij.net
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=api.jetbrains.ai
add list=JETBRAINS-CIDR comment=JETBRAINS-CIDR address=api.ai.jetbrains.com.cn
