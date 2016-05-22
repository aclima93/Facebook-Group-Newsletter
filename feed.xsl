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

                <hr/>

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
        <div class="w3-container w3-black w3-margin-bottom" align="center">

            <!-- Header of the story -->
            <h2>
                <xsl:choose>
                    <xsl:when test="@story">
                        <xsl:value-of select="@story"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <div>
                            <!-- template for from -->
                            <xsl:apply-templates select="from"/>
                            <br/>
                            <xsl:value-of select="@created_time"/>
                        </div>
                    </xsl:otherwise>
                </xsl:choose>
            </h2>

            <div class="w3-container w3-white">


                <!-- Image or Video -->
                <xsl:apply-templates select="picture_video"/>

                <!-- Message -->
                <xsl:value-of select="@message"/>

                <xsl:if test="comments">
                    <div class="w3-margin-top w3-container w3-blue">
                        <h4>Comentários</h4>

                        <!-- template for comments -->
                        <xsl:apply-templates select="comments"/>

                    </div>
                </xsl:if>

            </div>
        </div>

        <hr style="border: 1px solid #000" />

    </xsl:template>

    <xsl:template match="picture_video">

            <!-- link and accompanying image -->
            <xsl:variable name="link_variable"><xsl:value-of select="@link"/></xsl:variable>
            <a href="{$link_variable}" target="_blank">
                <xsl:choose>
                    <xsl:when test="@full_picture">
                        <xsl:variable name="picture_variable"><xsl:value-of select="@full_picture"/></xsl:variable>
                        <img src="{$picture_variable}"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="@link"/>
                    </xsl:otherwise>
                </xsl:choose>

            </a>

    </xsl:template>

    <xsl:template match="comments">

        <div class="w3-margin-top w3-container w3-black">

            <!-- Image or Video -->
            <xsl:apply-templates select="attatchment"/>

            <table>
                <!-- template for from -->
                <tr>
                    <td>
                        <xsl:apply-templates select="from"/>
                    </td>
                    <xsl:if test="@created_time">
                        <td>
                            Criado: <xsl:value-of select="@created_time"/>
                        </td>
                    </xsl:if>
                    <xsl:if test="@created_time">
                        <td>
                            Actualizado: <xsl:value-of select="@updated_time"/>
                        </td>
                    </xsl:if>
                </tr>
            </table>

            <div class="w3-margin-top w3-container w3-white">
                <xsl:value-of select="@message"/>

                <xsl:if test="replies">
                    <div class="w3-margin-bottom w3-container w3-margin-left w3-blue">
                        <!-- template for replies -->
                        <h4>Respostas</h4>

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

        <div class="w3-margin-top w3-container w3-black">

            <!-- Image or Video -->
            <xsl:apply-templates select="attatchment"/>

            <div >
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