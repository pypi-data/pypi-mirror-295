from __future__ import annotations

mime_types = """
application/andrew-inset			ez
application/applixware				aw
application/atom+xml				atom
application/atomcat+xml				atomcat
application/atomsvc+xml				atomsvc
application/ccxml+xml				ccxml
application/cdmi-capability			cdmia
application/cdmi-container			cdmic
application/cdmi-domain				cdmid
application/cdmi-object				cdmio
application/cdmi-queue				cdmiq
application/cu-seeme				cu
application/davmount+xml			davmount
application/docbook+xml				dbk
application/dssc+der				dssc
application/dssc+xml				xdssc
application/ecmascript				ecma
application/emma+xml				emma
application/epub+zip				epub
application/exi					exi
application/font-tdpfr				pfr
application/gml+xml				gml
application/gpx+xml				gpx
application/gxf					gxf
application/hyperstudio				stk
application/inkml+xml				ink inkml
application/ipfix				ipfix
application/java-archive			jar
application/java-serialized-object		ser
application/java-vm				class
application/javascript				js
application/json				json
application/jsonml+json				jsonml
application/lost+xml				lostxml
application/mac-binhex40			hqx
application/mac-compactpro			cpt
application/mads+xml				mads
application/marc				mrc
application/marcxml+xml				mrcx
application/mathematica				ma nb mb
application/mathml+xml				mathml
application/mbox				mbox
application/mediaservercontrol+xml		mscml
application/metalink+xml			metalink
application/metalink4+xml			meta4
application/mets+xml				mets
application/mods+xml				mods
application/mp21				m21 mp21
application/mp4					mp4s
application/msword				doc dot
application/mxf					mxf
application/octet-stream	bin dms lrf mar so dist distz pkg bpk dump elc deploy
application/oda					oda
application/oebps-package+xml			opf
application/ogg					ogx
application/omdoc+xml				omdoc
application/onenote				onetoc onetoc2 onetmp onepkg
application/oxps				oxps
application/patch-ops-error+xml			xer
application/pdf					pdf
application/pgp-encrypted			pgp
application/pgp-signature			asc sig
application/pics-rules				prf
application/pkcs10				p10
application/pkcs7-mime				p7m p7c
application/pkcs7-signature			p7s
application/pkcs8				p8
application/pkix-attr-cert			ac
application/pkix-cert				cer
application/pkix-crl				crl
application/pkix-pkipath			pkipath
application/pkixcmp				pki
application/pls+xml				pls
application/postscript				ai eps ps
application/prs.cww				cww
application/pskc+xml				pskcxml
application/rdf+xml				rdf
application/reginfo+xml				rif
application/relax-ng-compact-syntax		rnc
application/resource-lists+xml			rl
application/resource-lists-diff+xml		rld
application/rls-services+xml			rs
application/rpki-ghostbusters			gbr
application/rpki-manifest			mft
application/rpki-roa				roa
application/rsd+xml				rsd
application/rss+xml				rss
application/rtf					rtf
application/sbml+xml				sbml
application/scvp-cv-request			scq
application/scvp-cv-response			scs
application/scvp-vp-request			spq
application/scvp-vp-response			spp
application/sdp					sdp
application/set-payment-initiation		setpay
application/set-registration-initiation		setreg
application/shf+xml				shf
application/smil+xml				smi smil
application/sparql-query			rq
application/sparql-results+xml			srx
application/srgs				gram
application/srgs+xml				grxml
application/sru+xml				sru
application/ssdl+xml				ssdl
application/ssml+xml				ssml
application/tei+xml				tei teicorpus
application/thraud+xml				tfi
application/timestamped-data			tsd
application/vnd.3gpp.pic-bw-large		plb
application/vnd.3gpp.pic-bw-small		psb
application/vnd.3gpp.pic-bw-var			pvb
application/vnd.3gpp2.tcap			tcap
application/vnd.3m.post-it-notes		pwn
application/vnd.accpac.simply.aso		aso
application/vnd.accpac.simply.imp		imp
application/vnd.acucobol			acu
application/vnd.acucorp				atc acutc
application/vnd.adobe.air-application-installer-package+zip	air
application/vnd.adobe.formscentral.fcdt		fcdt
application/vnd.adobe.fxp			fxp fxpl
application/vnd.adobe.xdp+xml			xdp
application/vnd.adobe.xfdf			xfdf
application/vnd.ahead.space			ahead
application/vnd.airzip.filesecure.azf		azf
application/vnd.airzip.filesecure.azs		azs
application/vnd.amazon.ebook			azw
application/vnd.americandynamics.acc		acc
application/vnd.amiga.ami			ami
application/vnd.android.package-archive		apk
application/vnd.anser-web-certificate-issue-initiation	cii
application/vnd.anser-web-funds-transfer-initiation	fti
application/vnd.antix.game-component		atx
application/vnd.apple.installer+xml		mpkg
application/vnd.apple.mpegurl			m3u8
application/vnd.aristanetworks.swi		swi
application/vnd.astraea-software.iota		iota
application/vnd.audiograph			aep
application/vnd.blueice.multipass		mpm
application/vnd.bmi				bmi
application/vnd.businessobjects			rep
application/vnd.chemdraw+xml			cdxml
application/vnd.chipnuts.karaoke-mmd		mmd
application/vnd.cinderella			cdy
application/vnd.claymore			cla
application/vnd.cloanto.rp9			rp9
application/vnd.clonk.c4group			c4g c4d c4f c4p c4u
application/vnd.cluetrust.cartomobile-config		c11amc
application/vnd.cluetrust.cartomobile-config-pkg	c11amz
application/vnd.commonspace			csp
application/vnd.contact.cmsg			cdbcmsg
application/vnd.cosmocaller			cmc
application/vnd.crick.clicker			clkx
application/vnd.crick.clicker.keyboard		clkk
application/vnd.crick.clicker.palette		clkp
application/vnd.crick.clicker.template		clkt
application/vnd.crick.clicker.wordbank		clkw
application/vnd.criticaltools.wbs+xml		wbs
application/vnd.ctc-posml			pml
application/vnd.cups-ppd			ppd
application/vnd.curl.car			car
application/vnd.curl.pcurl			pcurl
application/vnd.dart				dart
application/vnd.data-vision.rdz			rdz
application/vnd.dece.data			uvf uvvf uvd uvvd
application/vnd.dece.ttml+xml			uvt uvvt
application/vnd.dece.unspecified		uvx uvvx
application/vnd.dece.zip			uvz uvvz
application/vnd.denovo.fcselayout-link		fe_launch
application/vnd.dna				dna
application/vnd.dolby.mlp			mlp
application/vnd.dpgraph				dpg
application/vnd.dreamfactory			dfac
application/vnd.ds-keypoint			kpxx
application/vnd.dvb.ait				ait
application/vnd.dvb.service			svc
application/vnd.dynageo				geo
application/vnd.ecowin.chart			mag
application/vnd.enliven				nml
application/vnd.epson.esf			esf
application/vnd.epson.msf			msf
application/vnd.epson.quickanime		qam
application/vnd.epson.salt			slt
application/vnd.epson.ssf			ssf
application/vnd.eszigno3+xml			es3 et3
application/vnd.ezpix-album			ez2
application/vnd.ezpix-package			ez3
application/vnd.fdf				fdf
application/vnd.fdsn.mseed			mseed
application/vnd.fdsn.seed			seed dataless
application/vnd.flographit			gph
application/vnd.fluxtime.clip			ftc
application/vnd.framemaker			fm frame maker book
application/vnd.frogans.fnc			fnc
application/vnd.frogans.ltf			ltf
application/vnd.fsc.weblaunch			fsc
application/vnd.fujitsu.oasys			oas
application/vnd.fujitsu.oasys2			oa2
application/vnd.fujitsu.oasys3			oa3
application/vnd.fujitsu.oasysgp			fg5
application/vnd.fujitsu.oasysprs		bh2
application/vnd.fujixerox.ddd			ddd
application/vnd.fujixerox.docuworks		xdw
application/vnd.fujixerox.docuworks.binder	xbd
application/vnd.fuzzysheet			fzs
application/vnd.genomatix.tuxedo		txd
application/vnd.geogebra.file			ggb
application/vnd.geogebra.tool			ggt
application/vnd.geometry-explorer		gex gre
application/vnd.geonext				gxt
application/vnd.geoplan				g2w
application/vnd.geospace			g3w
application/vnd.gmx				gmx
application/vnd.google-earth.kml+xml		kml
application/vnd.google-earth.kmz		kmz
application/vnd.grafeq				gqf gqs
application/vnd.groove-account			gac
application/vnd.groove-help			ghf
application/vnd.groove-identity-message		gim
application/vnd.groove-injector			grv
application/vnd.groove-tool-message		gtm
application/vnd.groove-tool-template		tpl
application/vnd.groove-vcard			vcg
application/vnd.hal+xml				hal
application/vnd.handheld-entertainment+xml	zmm
application/vnd.hbci				hbci
application/vnd.hhe.lesson-player		les
application/vnd.hp-hpgl				hpgl
application/vnd.hp-hpid				hpid
application/vnd.hp-hps				hps
application/vnd.hp-jlyt				jlt
application/vnd.hp-pcl				pcl
application/vnd.hp-pclxl			pclxl
application/vnd.hydrostatix.sof-data		sfd-hdstx
application/vnd.ibm.minipay			mpy
application/vnd.ibm.modcap			afp listafp list3820
application/vnd.ibm.rights-management		irm
application/vnd.ibm.secure-container		sc
application/vnd.iccprofile			icc icm
application/vnd.igloader			igl
application/vnd.immervision-ivp			ivp
application/vnd.immervision-ivu			ivu
application/vnd.insors.igm			igm
application/vnd.intercon.formnet		xpw xpx
application/vnd.intergeo			i2g
application/vnd.intu.qbo			qbo
application/vnd.intu.qfx			qfx
application/vnd.ipunplugged.rcprofile		rcprofile
application/vnd.irepository.package+xml		irp
application/vnd.is-xpr				xpr
application/vnd.isac.fcs			fcs
application/vnd.jam				jam
application/vnd.jcp.javame.midlet-rms		rms
application/vnd.jisp				jisp
application/vnd.joost.joda-archive		joda
application/vnd.kahootz				ktz ktr
application/vnd.kde.karbon			karbon
application/vnd.kde.kchart			chrt
application/vnd.kde.kformula			kfo
application/vnd.kde.kivio			flw
application/vnd.kde.kontour			kon
application/vnd.kde.kpresenter			kpr kpt
application/vnd.kde.kspread			ksp
application/vnd.kde.kword			kwd kwt
application/vnd.kenameaapp			htke
application/vnd.kidspiration			kia
application/vnd.kinar				kne knp
application/vnd.koan				skp skd skt skm
application/vnd.kodak-descriptor		sse
application/vnd.las.las+xml			lasxml
application/vnd.llamagraphics.life-balance.desktop	lbd
application/vnd.llamagraphics.life-balance.exchange+xml	lbe
application/vnd.lotus-1-2-3			123
application/vnd.lotus-approach			apr
application/vnd.lotus-freelance			pre
application/vnd.lotus-notes			nsf
application/vnd.lotus-organizer			org
application/vnd.lotus-screencam			scm
application/vnd.lotus-wordpro			lwp
application/vnd.macports.portpkg		portpkg
application/vnd.mcd				mcd
application/vnd.medcalcdata			mc1
application/vnd.mediastation.cdkey		cdkey
application/vnd.mfer				mwf
application/vnd.mfmp				mfm
application/vnd.micrografx.flo			flo
application/vnd.micrografx.igx			igx
application/vnd.mif				mif
application/vnd.mobius.daf			daf
application/vnd.mobius.dis			dis
application/vnd.mobius.mbk			mbk
application/vnd.mobius.mqy			mqy
application/vnd.mobius.msl			msl
application/vnd.mobius.plc			plc
application/vnd.mobius.txf			txf
application/vnd.mophun.application		mpn
application/vnd.mophun.certificate		mpc
application/vnd.mozilla.xul+xml			xul
application/vnd.ms-artgalry			cil
application/vnd.ms-cab-compressed		cab
application/vnd.ms-excel			xls xlm xla xlc xlt xlw
application/vnd.ms-excel.addin.macroenabled.12		xlam
application/vnd.ms-excel.sheet.binary.macroenabled.12	xlsb
application/vnd.ms-excel.sheet.macroenabled.12		xlsm
application/vnd.ms-excel.template.macroenabled.12	xltm
application/vnd.ms-fontobject			eot
application/vnd.ms-htmlhelp			chm
application/vnd.ms-ims				ims
application/vnd.ms-lrm				lrm
application/vnd.ms-officetheme			thmx
application/vnd.ms-pki.seccat			cat
application/vnd.ms-pki.stl			stl
application/vnd.ms-powerpoint			ppt pps pot
application/vnd.ms-powerpoint.addin.macroenabled.12		ppam
application/vnd.ms-powerpoint.presentation.macroenabled.12	pptm
application/vnd.ms-powerpoint.slide.macroenabled.12		sldm
application/vnd.ms-powerpoint.slideshow.macroenabled.12		ppsm
application/vnd.ms-powerpoint.template.macroenabled.12		potm
application/vnd.ms-project			mpp mpt
application/vnd.ms-word.document.macroenabled.12	docm
application/vnd.ms-word.template.macroenabled.12	dotm
application/vnd.ms-works			wps wks wcm wdb
application/vnd.ms-wpl				wpl
application/vnd.ms-xpsdocument			xps
application/vnd.mseq				mseq
application/vnd.musician			mus
application/vnd.muvee.style			msty
application/vnd.mynfc				taglet
application/vnd.neurolanguage.nlu		nlu
application/vnd.nitf				ntf nitf
application/vnd.noblenet-directory		nnd
application/vnd.noblenet-sealer			nns
application/vnd.noblenet-web			nnw
application/vnd.nokia.n-gage.data		ngdat
application/vnd.nokia.n-gage.symbian.install	n-gage
application/vnd.nokia.radio-preset		rpst
application/vnd.nokia.radio-presets		rpss
application/vnd.novadigm.edm			edm
application/vnd.novadigm.edx			edx
application/vnd.novadigm.ext			ext
application/vnd.oasis.opendocument.chart		odc
application/vnd.oasis.opendocument.chart-template	otc
application/vnd.oasis.opendocument.database		odb
application/vnd.oasis.opendocument.formula		odf
application/vnd.oasis.opendocument.formula-template	odft
application/vnd.oasis.opendocument.graphics		odg
application/vnd.oasis.opendocument.graphics-template	otg
application/vnd.oasis.opendocument.image		odi
application/vnd.oasis.opendocument.image-template	oti
application/vnd.oasis.opendocument.presentation		odp
application/vnd.oasis.opendocument.presentation-template	otp
application/vnd.oasis.opendocument.spreadsheet		ods
application/vnd.oasis.opendocument.spreadsheet-template	ots
application/vnd.oasis.opendocument.text			odt
application/vnd.oasis.opendocument.text-master		odm
application/vnd.oasis.opendocument.text-template	ott
application/vnd.oasis.opendocument.text-web		oth
application/vnd.olpc-sugar			xo
application/vnd.oma.dd2+xml			dd2
application/vnd.openofficeorg.extension		oxt
application/vnd.openxmlformats-officedocument.presentationml.presentation	pptx
application/vnd.openxmlformats-officedocument.presentationml.slide	sldx
application/vnd.openxmlformats-officedocument.presentationml.slideshow	ppsx
application/vnd.openxmlformats-officedocument.presentationml.template	potx
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet	xlsx
application/vnd.openxmlformats-officedocument.spreadsheetml.template	xltx
application/vnd.openxmlformats-officedocument.wordprocessingml.document	docx
application/vnd.openxmlformats-officedocument.wordprocessingml.template	dotx
application/vnd.osgeo.mapguide.package		mgp
application/vnd.osgi.dp				dp
application/vnd.osgi.subsystem			esa
application/vnd.palm				pdb pqa oprc
application/vnd.pawaafile			paw
application/vnd.pg.format			str
application/vnd.pg.osasli			ei6
application/vnd.picsel				efif
application/vnd.pmi.widget			wg
application/vnd.pocketlearn			plf
application/vnd.powerbuilder6			pbd
application/vnd.previewsystems.box		box
application/vnd.proteus.magazine		mgz
application/vnd.publishare-delta-tree		qps
application/vnd.pvi.ptid1			ptid
application/vnd.quark.quarkxpress		qxd qxt qwd qwt qxl qxb
application/vnd.realvnc.bed			bed
application/vnd.recordare.musicxml		mxl
application/vnd.recordare.musicxml+xml		musicxml
application/vnd.rig.cryptonote			cryptonote
application/vnd.rim.cod				cod
application/vnd.rn-realmedia			rm
application/vnd.rn-realmedia-vbr		rmvb
application/vnd.route66.link66+xml		link66
application/vnd.sailingtracker.track		st
application/vnd.seemail				see
application/vnd.sema				sema
application/vnd.semd				semd
application/vnd.semf				semf
application/vnd.shana.informed.formdata		ifm
application/vnd.shana.informed.formtemplate	itp
application/vnd.shana.informed.interchange	iif
application/vnd.shana.informed.package		ipk
application/vnd.simtech-mindmapper		twd twds
application/vnd.smaf				mmf
application/vnd.smart.teacher			teacher
application/vnd.solent.sdkm+xml			sdkm sdkd
application/vnd.spotfire.dxp			dxp
application/vnd.spotfire.sfs			sfs
application/vnd.stardivision.calc		sdc
application/vnd.stardivision.draw		sda
application/vnd.stardivision.impress		sdd
application/vnd.stardivision.math		smf
application/vnd.stardivision.writer		sdw vor
application/vnd.stardivision.writer-global	sgl
application/vnd.stepmania.package		smzip
application/vnd.stepmania.stepchart		sm
application/vnd.sun.xml.calc			sxc
application/vnd.sun.xml.calc.template		stc
application/vnd.sun.xml.draw			sxd
application/vnd.sun.xml.draw.template		std
application/vnd.sun.xml.impress			sxi
application/vnd.sun.xml.impress.template	sti
application/vnd.sun.xml.math			sxm
application/vnd.sun.xml.writer			sxw
application/vnd.sun.xml.writer.global		sxg
application/vnd.sun.xml.writer.template		stw
application/vnd.sus-calendar			sus susp
application/vnd.svd				svd
application/vnd.symbian.install			sis sisx
application/vnd.syncml+xml			xsm
application/vnd.syncml.dm+wbxml			bdm
application/vnd.syncml.dm+xml			xdm
application/vnd.tao.intent-module-archive	tao
application/vnd.tcpdump.pcap			pcap cap dmp
application/vnd.tmobile-livetv			tmo
application/vnd.trid.tpt			tpt
application/vnd.triscape.mxs			mxs
application/vnd.trueapp				tra
application/vnd.ufdl				ufd ufdl
application/vnd.uiq.theme			utz
application/vnd.umajin				umj
application/vnd.unity				unityweb
application/vnd.uoml+xml			uoml
application/vnd.vcx				vcx
application/vnd.visio				vsd vst vss vsw
application/vnd.visionary			vis
application/vnd.vsf				vsf
application/vnd.wap.wbxml			wbxml
application/vnd.wap.wmlc			wmlc
application/vnd.wap.wmlscriptc			wmlsc
application/vnd.webturbo			wtb
application/vnd.wolfram.player			nbp
application/vnd.wordperfect			wpd
application/vnd.wqd				wqd
application/vnd.wt.stf				stf
application/vnd.xara				xar
application/vnd.xfdl				xfdl
application/vnd.yamaha.hv-dic			hvd
application/vnd.yamaha.hv-script		hvs
application/vnd.yamaha.hv-voice			hvp
application/vnd.yamaha.openscoreformat			osf
application/vnd.yamaha.openscoreformat.osfpvg+xml	osfpvg
application/vnd.yamaha.smaf-audio		saf
application/vnd.yamaha.smaf-phrase		spf
application/vnd.yellowriver-custom-menu		cmp
application/vnd.zul				zir zirz
application/vnd.zzazz.deck+xml			zaz
application/voicexml+xml			vxml
application/widget				wgt
application/winhlp				hlp
application/wsdl+xml				wsdl
application/wspolicy+xml			wspolicy
application/x-7z-compressed			7z
application/x-abiword				abw
application/x-ace-compressed			ace
application/x-apple-diskimage			dmg
application/x-authorware-bin			aab x32 u32 vox
application/x-authorware-map			aam
application/x-authorware-seg			aas
application/x-bcpio				bcpio
application/x-bittorrent			torrent
application/x-blorb				blb blorb
application/x-bzip				bz
application/x-bzip2				bz2 boz
application/x-cbr				cbr cba cbt cbz cb7
application/x-cdlink				vcd
application/x-cfs-compressed			cfs
application/x-chat				chat
application/x-chess-pgn				pgn
application/x-conference			nsc
application/x-cpio				cpio
application/x-csh				csh
application/x-debian-package			deb udeb
application/x-dgc-compressed			dgc
application/x-director			dir dcr dxr cst cct cxt w3d fgd swa
application/x-doom				wad
application/x-dtbncx+xml			ncx
application/x-dtbook+xml			dtb
application/x-dtbresource+xml			res
application/x-dvi				dvi
application/x-envoy				evy
application/x-eva				eva
application/x-font-bdf				bdf
application/x-font-ghostscript			gsf
application/x-font-linux-psf			psf
application/x-font-pcf				pcf
application/x-font-snf				snf
application/x-font-type1			pfa pfb pfm afm
application/x-freearc				arc
application/x-futuresplash			spl
application/x-gca-compressed			gca
application/x-glulx				ulx
application/x-gnumeric				gnumeric
application/x-gramps-xml			gramps
application/x-gtar				gtar
application/x-hdf				hdf
application/x-install-instructions		install
application/x-iso9660-image			iso
application/x-java-jnlp-file			jnlp
application/x-latex				latex
application/x-lzh-compressed			lzh lha
application/x-mie				mie
application/x-mobipocket-ebook			prc mobi
application/x-ms-application			application
application/x-ms-shortcut			lnk
application/x-ms-wmd				wmd
application/x-ms-wmz				wmz
application/x-ms-xbap				xbap
application/x-msaccess				mdb
application/x-msbinder				obd
application/x-mscardfile			crd
application/x-msclip				clp
application/x-msdownload			exe dll com bat msi
application/x-msmediaview			mvb m13 m14
application/x-msmetafile			wmf wmz emf emz
application/x-msmoney				mny
application/x-mspublisher			pub
application/x-msschedule			scd
application/x-msterminal			trm
application/x-mswrite				wri
application/x-netcdf				nc cdf
application/x-nzb				nzb
application/x-pkcs12				p12 pfx
application/x-pkcs7-certificates		p7b spc
application/x-pkcs7-certreqresp			p7r
application/x-rar-compressed			rar
application/x-research-info-systems		ris
application/x-sh				sh
application/x-shar				shar
application/x-shockwave-flash			swf
application/x-silverlight-app			xap
application/x-sql				sql
application/x-stuffit				sit
application/x-stuffitx				sitx
application/x-subrip				srt
application/x-sv4cpio				sv4cpio
application/x-sv4crc				sv4crc
application/x-t3vm-image			t3
application/x-tads				gam
application/x-tar				tar
application/x-tcl				tcl
application/x-tex				tex
application/x-tex-tfm				tfm
application/x-texinfo				texinfo texi
application/x-tgif				obj
application/x-ustar				ustar
application/x-wais-source			src
application/x-x509-ca-cert			der crt
application/x-xfig				fig
application/x-xliff+xml				xlf
application/x-xpinstall				xpi
application/x-xz				xz
application/x-zmachine				z1 z2 z3 z4 z5 z6 z7 z8
application/xaml+xml				xaml
application/xcap-diff+xml			xdf
application/xenc+xml				xenc
application/xhtml+xml				xhtml xht
application/xml					xml xsl
application/xml-dtd				dtd
application/xop+xml				xop
application/xproc+xml				xpl
application/xslt+xml				xslt
application/xspf+xml				xspf
application/xv+xml				mxml xhvml xvml xvm
application/yang				yang
application/yin+xml				yin
application/zip					zip
audio/adpcm					adp
audio/basic					au snd
audio/midi					mid midi kar rmi
audio/mp4					m4a mp4a
audio/mpeg					mp3 mpga mp2 mp2a m2a m3a
audio/ogg					ogg oga spx
audio/s3m					s3m
audio/silk					sil
audio/vnd.dece.audio				uva uvva
audio/vnd.digital-winds				eol
audio/vnd.dra					dra
audio/vnd.dts					dts
audio/vnd.dts.hd				dtshd
audio/vnd.lucent.voice				lvp
audio/vnd.ms-playready.media.pya		pya
audio/vnd.nuera.ecelp4800			ecelp4800
audio/vnd.nuera.ecelp7470			ecelp7470
audio/vnd.nuera.ecelp9600			ecelp9600
audio/vnd.rip					rip
audio/webm					weba
audio/x-aac					aac
audio/x-aiff					aif aiff aifc
audio/x-caf					caf
audio/x-flac					flac
audio/x-matroska				mka
audio/x-mpegurl					m3u
audio/x-ms-wax					wax
audio/x-ms-wma					wma
audio/x-pn-realaudio				ram ra
audio/x-pn-realaudio-plugin			rmp
audio/x-wav					wav
audio/xm					xm
chemical/x-cdx					cdx
chemical/x-cif					cif
chemical/x-cmdf					cmdf
chemical/x-cml					cml
chemical/x-csml					csml
chemical/x-xyz					xyz
font/collection					ttc
font/otf					otf
font/ttf					ttf
font/woff					woff
font/woff2					woff2
image/bmp					bmp
image/cgm					cgm
image/g3fax					g3
image/gif					gif
image/ief					ief
image/jpeg					jpg jpeg jpe
image/ktx					ktx
image/png					png
image/prs.btif					btif
image/sgi					sgi
image/svg+xml					svg svgz
image/tiff					tiff tif
image/vnd.adobe.photoshop			psd
image/vnd.dece.graphic				uvi uvvi uvg uvvg
image/vnd.djvu					djvu djv
image/vnd.dvb.subtitle				sub
image/vnd.dwg					dwg
image/vnd.dxf					dxf
image/vnd.fastbidsheet				fbs
image/vnd.fpx					fpx
image/vnd.fst					fst
image/vnd.fujixerox.edmics-mmr			mmr
image/vnd.fujixerox.edmics-rlc			rlc
image/vnd.ms-modi				mdi
image/vnd.ms-photo				wdp
image/vnd.net-fpx				npx
image/vnd.wap.wbmp				wbmp
image/vnd.xiff					xif
image/webp					webp
image/x-3ds					3ds
image/x-cmu-raster				ras
image/x-cmx					cmx
image/x-freehand				fh fhc fh4 fh5 fh7
image/x-icon					ico
image/x-mrsid-image				sid
image/x-pcx					pcx
image/x-pict					pic pct
image/x-portable-anymap				pnm
image/x-portable-bitmap				pbm
image/x-portable-graymap			pgm
image/x-portable-pixmap				ppm
image/x-rgb					rgb
image/x-tga					tga
image/x-xbitmap					xbm
image/x-xpixmap					xpm
image/x-xwindowdump				xwd
message/rfc822					eml mime
model/iges					igs iges
model/mesh					msh mesh silo
model/vnd.collada+xml				dae
model/vnd.dwf					dwf
model/vnd.gdl					gdl
model/vnd.gtw					gtw
model/vnd.mts					mts
model/vnd.vtu					vtu
model/vrml					wrl vrml
model/x3d+binary				x3db x3dbz
model/x3d+vrml					x3dv x3dvz
model/x3d+xml					x3d x3dz
text/cache-manifest				appcache
text/calendar					ics ifb
text/css					css
text/csv					csv
text/html					html htm
text/n3						n3
text/plain					txt text conf def list log in
text/prs.lines.tag				dsc
text/richtext					rtx
text/sgml					sgml sgm
text/tab-separated-values			tsv
text/troff					t tr roff man me ms
text/turtle					ttl
text/uri-list					uri uris urls
text/vcard					vcard
text/vnd.curl					curl
text/vnd.curl.dcurl				dcurl
text/vnd.curl.mcurl				mcurl
text/vnd.curl.scurl				scurl
text/vnd.dvb.subtitle				sub
text/vnd.fly					fly
text/vnd.fmi.flexstor				flx
text/vnd.graphviz				gv
text/vnd.in3d.3dml				3dml
text/vnd.in3d.spot				spot
text/vnd.sun.j2me.app-descriptor		jad
text/vnd.wap.wml				wml
text/vnd.wap.wmlscript				wmls
text/x-asm					s asm
text/x-c					c cc cxx cpp h hh dic
text/x-fortran					f for f77 f90
text/x-java-source				java
text/x-nfo					nfo
text/x-opml					opml
text/x-pascal					p pas
text/x-setext					etx
text/x-sfv					sfv
text/x-uuencode					uu
text/x-vcalendar				vcs
text/x-vcard					vcf
video/3gpp					3gp
video/3gpp2					3g2
video/h261					h261
video/h263					h263
video/h264					h264
video/jpeg					jpgv
video/jpm					jpm jpgm
video/mj2					mj2 mjp2
video/mp4					mp4 mp4v mpg4
video/mpeg					mpeg mpg mpe m1v m2v
video/ogg					ogv
video/quicktime					qt mov
video/vnd.dece.hd				uvh uvvh
video/vnd.dece.mobile				uvm uvvm
video/vnd.dece.pd				uvp uvvp
video/vnd.dece.sd				uvs uvvs
video/vnd.dece.video				uvv uvvv
video/vnd.dvb.file				dvb
video/vnd.fvt					fvt
video/vnd.mpegurl				mxu m4u
video/vnd.ms-playready.media.pyv		pyv
video/vnd.uvvu.mp4				uvu uvvu
video/vnd.vivo					viv
video/webm					webm
video/x-f4v					f4v
video/x-fli					fli
video/x-flv					flv
video/x-m4v					m4v
video/x-matroska				mkv mk3d mks
video/x-mng					mng
video/x-ms-asf					asf asx
video/x-ms-vob					vob
video/x-ms-wm					wm
video/x-ms-wmv					wmv
video/x-ms-wmx					wmx
video/x-ms-wvx					wvx
video/x-msvideo					avi
video/x-sgi-movie				movie
video/x-smv					smv
x-conference/x-cooltalk				ice
application/x-bad-tgsticker		tgs
application/x-tgsticker		tgs
"""
