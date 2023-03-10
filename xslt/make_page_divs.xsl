<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="#all" xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    version="2.0">
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="node() | @*"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="body/div">
        <xsl:for-each-group select="*" group-starting-with="tei:pb">
            <div xmlns="http://www.tei-c.org/ns/1.0" type="page">
                <xsl:apply-templates select="current-group()"/>
            </div>
        </xsl:for-each-group>
    </xsl:template>
    <xsl:template match="body[./pb]">
        <body xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:for-each-group select="*" group-starting-with="tei:pb">
                <div xmlns="http://www.tei-c.org/ns/1.0" type="page">
                    <xsl:apply-templates select="current-group()"/>
                </div>
            </xsl:for-each-group>
        </body>
        
    </xsl:template>

    <xsl:template match="tei:body//tei:ab">
        <p xmlns="http://www.tei-c.org/ns/1.0">
            <xsl:apply-templates select="@* | node()"/>
        </p>
    </xsl:template>

    <xsl:template match="tei:lb">
        <xsl:copy>
            <xsl:attribute name="n">
                <xsl:value-of select="@n"/>
            </xsl:attribute>
            <xsl:apply-templates select="node()"/>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
