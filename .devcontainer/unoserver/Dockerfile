# Use the base image from ghcr.io/unoconv/unoserver-docker
FROM ghcr.io/unoconv/unoserver-docker

# As root
USER root

ARG FONTS_FOLDER=/usr/share/fonts

# [Custom Font] Install custom fonts (copy font files)
# Place font files in the `./unoserver/customfonts` folder
# to ensure they are installed during the build process.
COPY unoserver/customfonts ${FONTS_FOLDER}/customfonts
RUN fc-cache -vf

# [IPA Font] Install Japanese fonts
# ###################################
#   IPA FONT LICENSE AGREEMENT V1.0
# https://moji.or.jp/ipafont/license/
# ###################################
COPY unoserver/ipafonts /usr/local/ipafonts
WORKDIR /usr/local/ipafonts
RUN apk --no-cache add wget \
    # Download ipa fonts
    && wget -i urls.txt \
    # Installed fonts folder
    && mkdir -p ${FONTS_FOLDER}/ipa \
	# IPAmj Mincho Font
    && unzip ipamjm00601.zip -d ${FONTS_FOLDER}/ipa/ipamjm0601 \
    # IPAex Font（2 fonts）
    && unzip IPAexfont00401.zip -d ${FONTS_FOLDER}/ipa/ipaexfont00401 \
    # IPA Font（4 fonts）
    && unzip IPAfont00303.zip -d ${FONTS_FOLDER}/ipa/ipafont00303 \
    # Build font information cache files
    && fc-cache -vf

# As worker
USER ${UID}
WORKDIR ${HOME}
