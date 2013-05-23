#!/bin/bash
# TOMADO DEL PAQUETE KEYBOARD-CONFIGURATION DE DEBIAN
# Este script está conformado por partes de código contenido en el paquete de 
# Debian keyboard-configuration, especificamente del archivo
# /var/lib/dpkg/info/keyboard-configuration.config el cual entre otras cosas se
# encarga de asociar en idioma seleccionado con la configuración del teclado
# correspondiente.
# 
# OJO:
# Verificar este archivo para mantenerlo siempre actualizado con las mejoras que
# pueda hacer debian

#if type locale 2>/dev/null >/dev/null; then
#    eval `locale`
#fi

#if [ "$LC_CTYPE"  -a "$LC_CTYPE" != C ]; then
#    locale=$LC_CTYPE
#else
#    locale=C
#fi


if [ "$1" -a "$1" != C ]; then
    locale=$1
else
    echo "No se ha indicado un valor de LOCALE" 1>&2
    exit 1
fi

guess_arch () {
    local arch subarch line

    if type archdetect 2>/dev/null >/dev/null; then
        archdetect
        return 0
    fi

    arch=`dpkg --print-architecture`

    if [ "$arch" = 'powerpc' -o "$arch" = 'm68k' ]; then
        if [ "$arch" = powerpc ]; then
            line=`sed -n 's/^platform.*: *//p' /proc/cpuinfo`
            if [ "$line" = PS3 ] || [ "$line" = Cell ]; then
                subarch=`echo $line|tr A-Z a-z`
            else
                line=`sed -n 's/^machine.*: *//p' /proc/cpuinfo`
                if [ "$line" = '' ]; then
                    echo unknown
                    return 0
                fi
                subarch=`echo $line|tr A-Z a-z`
            fi
        elif [ "$arch" = m68k ]; then
            line=`sed -n 's/^Model.*: *//p' /proc/hardware`
            if [ "$line" = '' ]; then
                echo unknown
                return 0
            fi
            subarch=`echo $line|tr A-Z a-z`
        fi
        case "$subarch" in
            *amiga*)
                subarch=amiga
                ;;
            *chrp*)
                subarch=chrp
                ;;
            *prep*)
                subarch=prep
                ;;
            *macintosh*|*powermac*|*powerbook*|*power*|*imac*|*powermac1*)
                subarch=mac
                ;;
            *atari*)
                subarch=atari
                ;;
            *motorola*)
                subarch=mvme
                ;;
            *bvme*)
                subarch=bvme
                ;;
            *)
                subarch=`echo $subarch|sed  's/^\s*//'`
                ;;
        esac
        arch="$arch/$subarch"
    fi
    echo $arch
    return 0
}

arch=`guess_arch`

case "$arch" in
    alpha*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    amd64*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    arm*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    i386*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    hppa*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    ia64*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    m68k/amiga)
	XKBMODEL=amiga
	model_priority=medium
	;;
    m68k/atari)
	XKBMODEL=ataritt
	model_priority=medium
	;;
    m68k/mac)
	XKBMODEL=macintosh_old
	model_priority=medium
	;;
    m68k/sun*)
	XKBMODEL=pc105 # UNKNOWN: sun4, sun5 or pc105
	model_priority=critical
	;;
    m68k/*vme*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    mips*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    powerpc/amiga)
	XKBMODEL=amiga
	model_priority=medium
	;;
    powerpc/apus)
	XKBMODEL=amiga
	model_priority=medium
	;;
    powerpc/chrp*)
	XKBMODEL=pc105 # UNKNOWN: pc105, macintosh_old or maybe amiga
	model_priority=critical
	;;
    powerpc/mac)
	XKBMODEL=pc105
	model_priority=medium
	;;
    powerpc/pasemi)
	XKBMODEL=pc105
	model_priority=medium
	;;
    powerpc/powermac*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    powerpc/prep)
	XKBMODEL=pc105
	model_priority=medium
	;;
    powerpc/ps3|powerpc/cell)
	XKBMODEL=pc105
	model_priority=medium
	;;
    sparc*)
	XKBMODEL=pc105 # sun4 or sun5 on older kernels
	model_priority=medium
	;;
    s390*)
	XKBMODEL=pc105
	model_priority=medium
	;;
    *)
	XKBMODEL=pc105 # UNKNOWN
	model_priority=critical
	;;
esac

layout_priority=critical
case "$locale" in
    # Keyboards for countries
    *_AL*)
	XKBLAYOUT=al  # Albania
	;;
    *_AZ*)
	XKBLAYOUT=az  # Azerbaijan
	;;
    *_BD*)
	XKBLAYOUT=us,bd  # Bangladesh
	;;
    *_BE*)
	XKBLAYOUT=be  # Belgium
	;;
    *_BG*)
	XKBLAYOUT=us,bg  # Bulgaria
	layout_priority=critical
	;;
    *_BR*)
	XKBLAYOUT=br  # Brazil
	;;
    *_BT*)
	XKBLAYOUT=us,bt  # Bhutan
	;;
    *_BY*)
	XKBLAYOUT=us,by  # Belarus
	;;
    fr_CA*)
	XKBLAYOUT=ca  # Canada
	;;
    *_CA*)
	XKBLAYOUT=us  # U.S. English
	;;
    de_CH*)
	XKBLAYOUT=ch  # Switzerland
	;;
    fr_CH*)
	XKBLAYOUT=ch  # Switzerland
	XKBVARIANT=fr # French
	;;
    *_CH*)
	XKBLAYOUT=ch  # Switzerland
	layout_priority=critical
	;;
    *_CZ*)
	XKBLAYOUT=cz  # Czechia
	layout_priority=critical
	;;
    *_DK*)
	XKBLAYOUT=dk  # Denmark
	;;
    *_EE*)
	XKBLAYOUT=ee  # Estonia
	;;
    ast_ES*)
	XKBLAYOUT=es  # Spain
	XKBVARIANT=ast # Asturian
	;;
    ca_ES*)
	XKBLAYOUT=es  # Spain
	XKBVARIANT=cat # Catalan
	;;
    *_ES*)
	XKBLAYOUT=es  # Spain
	;;
    *_ET*)
	XKBLAYOUT=us,et  # Ethiopia
	;;
    se_FI*)
	XKBLAYOUT=fi  # Finland
	XKBVARIANT=smi # Northern Saami
	;;
    *_FI*)
	XKBLAYOUT=fi  # Finland
	;;
    *_FR*)
	XKBLAYOUT=fr  # French
	XKBVARIANT=latin9
	;;
    *_GB*)
	XKBLAYOUT=gb  # United Kingdom
	;;
    *_GG*)
	XKBLAYOUT=gb  # United Kingdom
	;;
    *_HU*)
	XKBLAYOUT=hu  # Hungary
	;;
    *_IE*)
	XKBLAYOUT=ie  # Ireland
	;;
    *_IL*)
	XKBLAYOUT=us,il  # Israel
	layout_priority=critical
	;;
    *_IM*)
	XKBLAYOUT=gb  # United Kingdom
	;;
    *_IR*)
	XKBLAYOUT=us,ir  # Iran
	;;
    *_IS*)
	XKBLAYOUT=is  # Iceland
	;;
    *_IT*)
	XKBLAYOUT=it  # Italy
	;;
    *_JE*)
	XKBLAYOUT=gb  # United Kingdom
	;;
    *_JP*)
	XKBLAYOUT=jp  # Japan
	;;
    *_LT*)
	XKBLAYOUT=lt  # Lithuania
	layout_priority=critical
	;;
    *_LV*)
	XKBLAYOUT=lv  # Latvia
	;;
    *_KG*)
	XKBLAYOUT=us,kg  # Kyrgyzstan
	;;
    *_KH*)
	XKBLAYOUT=us,kh  # Cambodia
	;;
    *_KP*)
	XKBLAYOUT=kr  # Korea
	;;
    *_KZ*)
	XKBLAYOUT=us,kz  # Kazakhstan
	;;
    *_LK*)
	XKBLAYOUT=us,lk  # Sri Lanka
	;;
    *_MA*)
	XKBLAYOUT=us,ma  # Morocco
	;;
    *_MK*)
	XKBLAYOUT=us,mk  # Macedonia
	;;
    *_NL*)
	XKBLAYOUT=us  # Netherlands
	;;
    *_MN*)
	XKBLAYOUT=us,mn  # Mongolia
	;;
    *_MT*)
	XKBLAYOUT=mt  # Malta
	layout_priority=critical
	;;
    se_NO*)
	XKBLAYOUT=no  # Norway
	XKBVARIANT=smi # Northern Saami
	;;
    *_NO*)
	XKBLAYOUT=no  # Norway (se_NO is not in this case)
	;;
    *_NP*)
	XKBLAYOUT=us,np  # Nepal
	;;
    *_PL*)
	XKBLAYOUT=pl  # Poland
	;;
    *_PT*)
	XKBLAYOUT=pt  # Portugal
	;;
    *_RO*)
	XKBLAYOUT=ro  # Romania
	;;
    *_RU*)
	XKBLAYOUT=us,ru  # Russia
	layout_priority=critical
	;;
    se_SE*)
	XKBLAYOUT=se  # Sweden
	XKBVARIANT=smi # Northern Saami
	;;
    *_SK*)
	XKBLAYOUT=sk  # Slovakia
	;;
    *_SI*)
	XKBLAYOUT=si  # Slovenia
	;;
    *_TJ*)
	XKBLAYOUT=us,tj  # Tajikistan
	;;
    *_TH*)
	XKBLAYOUT=us,th  # Thailand
	layout_priority=critical
	;;
    *_TR*)
	XKBLAYOUT=tr  # Turkish
	layout_priority=critical
	;;
    *_UA*)
	XKBLAYOUT=us,ua  # Ukraine
	;;
    en_US*)
	XKBLAYOUT=us  # U.S. English
	;;
    *_VN*)
	XKBLAYOUT=vn  # Vietnam
	;;
    *_ZA*)
	XKBLAYOUT=za  # South Africa
	;;
    # Keyboards for specific languages and international keyboards:
    # TODO: Is the following list correct?
    *_AR*|*_BO*|*_CL*|*_CO*|*_CR*|*_DO*|*_EC*|*_GT*|*_HN*|*_MX*|*_NI*|*_PA*|*_PE*|es_PR*|*_PY*|*_SV*|es_US*|*_UY*|*_VE*)
	XKBLAYOUT=latam # Latin American
	;;
    ar_*)
	XKBLAYOUT=us,ara # Arabic
	;;
    bn_*)
	XKBLAYOUT=us,in  # India
	XKBVARIANT=,ben # Bengali
	;;
    bs_*)
	XKBLAYOUT=ba  # Bosnia and Herzegovina
	;;
    de_LI*)
	XKBLAYOUT=ch  # Liechtenstein
	;;
    de_*)
	XKBLAYOUT=de  # Germany
	;;
    el_*)
	XKBLAYOUT=us,gr  # Greece
	;;
    eo|eo.*|eo_*|eo\@*)
	XKBLAYOUT=epo  # Esperanto
	layout_priority=critical
	;;
    fr_*)
	XKBLAYOUT=fr  # France
	XKBVARIANT=latin9
	layout_priority=critical
	;;
    gu_*)
	XKBLAYOUT=us,in  # India
	XKBVARIANT=,guj # Gujarati
	;;
    hi_*)
	XKBLAYOUT=us,in  # India
	XKBVARIANT=,deva # Devanagari
	;;
    hr_*)
	XKBLAYOUT=hr  # Croatia
	;;
    hy_*)
	XKBLAYOUT=us,am  # Armenia
	;;
    ka_*)
	XKBLAYOUT=us,ge  # Georgia
	layout_priority=critical
	;;
    kn_*)
	XKBLAYOUT=us,in  # India
	XKBVARIANT=,kan # Kannada
	;;
    ku_*)
	XKBLAYOUT=tr  # Turkish
	XKBVARIANT=ku # Kurdish
	layout_priority=critical
	;;
    lo_*)
	XKBLAYOUT=us,la  # Laos
	;;
    ml_*)
	XKBLAYOUT=us,in  # India
	XKBVARIANT=,mal # Malayalam
	;;
    os_*)
	XKBLAYOUT=ru  # Russia
	XKBVARIANT=os  # Ossetian
	;;
    pa_*)
	XKBLAYOUT=us,in  # India
	XKBVARIANT=,guru # Gurmukhi
	;;
    si_*)
	XKBLAYOUT=us,si  # Sri Lanka
	XKBVARIANT=,sin_phonetic # Sinhala
	;;
    sr_*)
	XKBLAYOUT=cs,cs  # Serbia and Montenegro
	XKBVARIANT=latin,basic
	layout_priority=critical
	;;
    sv_*)
	XKBLAYOUT=se  # Sweden
	;;
    ta_*)
	XKBLAYOUT=us,in  # India
	XKBVARIANT=,tam # Tamil
	;;
    te_*)
	XKBLAYOUT=us,in  # India
	XKBVARIANT=,tel # Telugu
	;;
    ug_*)
	XKBLAYOUT=us,cn  # China
	XKBVARIANT=,uig # Uyghur
	;;
    zh_*)
	XKBLAYOUT=cn  # Chinese
	;;
    # Fallback
    *)
	XKBLAYOUT=us
	;;
esac

echo "$XKBLAYOUT/$XKBMODEL/$XKBVARIANT"
