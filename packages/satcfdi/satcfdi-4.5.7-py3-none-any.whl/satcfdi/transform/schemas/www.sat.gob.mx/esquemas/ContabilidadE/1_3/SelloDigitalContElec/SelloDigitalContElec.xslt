<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:sellodigital="www.sat.gob.mx/esquemas/ContabilidadE/1_1/SelloDigitalContElec" xmlns:sellodigitalB="http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/SelloDigitalContElec" version="2.0"><xsl:include href="../../../utilerias.xslt"/><xsl:output method="text" version="1.0" encoding="UTF-8" indent="no"/><xsl:template match="/">|<xsl:apply-templates select="/sellodigital:SelloDigitalContElec"/><xsl:apply-templates select="/sellodigitalB:SelloDigitalContElec"/>||</xsl:template><xsl:template match="sellodigital:SelloDigitalContElec"><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Version"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Folio"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@RFC"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@FechadeSello"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@sello"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@noCertificadoSAT"/></xsl:call-template></xsl:template><xsl:template match="sellodigitalB:SelloDigitalContElec"><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Version"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@Folio"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@RFC"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@FechadeSello"/></xsl:call-template><xsl:call-template name="Opcional"><xsl:with-param name="valor" select="./@sello"/></xsl:call-template><xsl:call-template name="Requerido"><xsl:with-param name="valor" select="./@noCertificadoSAT"/></xsl:call-template></xsl:template></xsl:stylesheet>