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
                        Esta semana não houve actividade no grupo.
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

            <!-- Link -->
            <!--
            <div class="w3-container">
                <xsl:variable name="story_hyperlink">https://www.facebook.com/<xsl:value-of select="@id"/></xsl:variable>
                <p><xsl:value-of select="@summary_data" disable-output-escaping="no"/></p>
                <div align="center">
                    <p><a href="{$story_hyperlink}" target="_blank">Story Link</a></p>
                </div>
            </div>
            -->

            <!-- Message -->
            <div class="w3-container w3-row-padding w3-margin-left w3-white">
                <xsl:value-of select="@message"/>


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

    <xsl:template match="comments">


        <div class="w3-margin-top w3-container w3-blue">

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