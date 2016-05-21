<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Header and Footer -->
    <xsl:include href="header_footer.xsl"/>

    <xsl:template match="/">
        <html>

            <meta name="viewport" content="width=device-width, initial-scale=1"/>
            <link rel="stylesheet" href="http://www.w3schools.com/lib/w3.css"/>
            <!-- <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"/> -->


            <body>

                <!-- Header -->
                <xsl:call-template name="header"/>

                <xsl:choose>
                    <xsl:when test="objects/stories">
                        <!-- Story Data -->
                        <xsl:apply-templates select="objects/stories"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <p><b>Esta semana não houve actividade no grupo.</b></p>
                    </xsl:otherwise>
                </xsl:choose>

                <!-- Footer -->
                <xsl:call-template name="footer"/>

            </body>

        </html>
    </xsl:template>

    <xsl:template match="stories">

        <!-- Story -->
        <div class="w3-container w3-blue w3-margin-bottom">
            <h2> <xsl:value-of select="@story"/> </h2>

            <!-- Message -->
            <div class="w3-container w3-row-padding w3-margin-left w3-white">
                <xsl:value-of select="@message"/>

                <!-- Image or Video -->
                <xsl:apply-templates select="picture_video"/>

                <xsl:if test="comments">
                    <div class="w3-margin-top w3-container w3-indigo">
                        <h4>Comentários</h4>

                        <!-- template for comments -->
                        <xsl:apply-templates select="comments"/>

                    </div>
                </xsl:if>

            </div>
        </div>

        <hr/>

    </xsl:template>

    <xsl:template match="picture_video">

        <xsl:if test="@source">
            <xsl:variable name="source_variable"><xsl:value-of select="@source"/></xsl:variable>
            <xsl:variable name="mime_type_variable"><xsl:value-of select="@mime_type"/></xsl:variable>
            <xsl:if test="@mime_type">
                <div align="center">

                    <xsl:choose>
                        <xsl:when test="@source_type = 'image' ">
                            <img src="{$source_variable}" />
                        </xsl:when>

                        <xsl:when test="@source_type = 'video' ">
                            <video controls="controls">
                                <source src="{$source_variable}" type="{$mime_type_variable}" />
                            </video>
                        </xsl:when>

                        <xsl:otherwise>
                            <video controls="controls">
                                <source src="{$source_variable}" type="{$mime_type_variable}" />
                                <img src="{$source_variable}" />
                            </video>
                        </xsl:otherwise>
                    </xsl:choose>

                </div>
            </xsl:if>
        </xsl:if>

    </xsl:template>

    <xsl:template match="comments">

        <div class="w3-margin-top w3-container w3-blue">

            <!-- Image or Video -->
            <xsl:apply-templates select="picture_video"/>

            <div class="w3-container" >

                <!-- template for from -->
                <xsl:apply-templates select="from"/>
                <br/>
                <xsl:value-of select="@created_time"/>

            </div>

            <div class="w3-margin-top w3-container w3-white">
                <xsl:value-of select="@message"/>

                <xsl:if test="replies">
                    <div class="w3-margin-bottom w3-container w3-margin-left w3-indigo">
                        <!-- template for replies -->
                        <h4>Respostas ao comentário</h4>

                        <xsl:apply-templates select="replies"/>
                    </div>
                </xsl:if>
            </div>

        </div>

    </xsl:template>

    <xsl:template match="from">

        <xsl:variable name="person_hyperlink">https://www.facebook.com/<xsl:value-of select="@id"/></xsl:variable>
        <a href="{$person_hyperlink}" target="_blank"> <xsl:value-of select="@name"/></a>

    </xsl:template>

    <xsl:template match="replies">

        <div class="w3-margin-top w3-container w3-blue">

            <!-- Image or Video -->
            <xsl:apply-templates select="picture_video"/>

            <div class="w3-container" >
                <!-- template for from -->
                <xsl:apply-templates select="from"/>
                <br/>
                <xsl:value-of select="@created_time"/>

            </div>

            <div class="w3-margin-top w3-container w3-white">
                <xsl:value-of select="@message"/>
            </div>
        </div>

    </xsl:template>

</xsl:stylesheet>