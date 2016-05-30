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
                    <xsl:when test="posts/stories">
                        <!-- Story Data -->
                        <xsl:apply-templates select="posts/stories"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <font color="white">
                            <p><b>Esta semana não houve actividade no grupo.</b></p>
                        </font>
                    </xsl:otherwise>
                </xsl:choose>

                <hr/>

                <!-- Footer -->
                <xsl:call-template name="footer"/>

            </body>

        </html>
    </xsl:template>

    <!--
    aux templates
    -->

    <!-- from template -->
    <xsl:template match="from">

        <table>
            <!-- name and accompanying image, with links -->
            <xsl:variable name="person_hyperlink">https://www.facebook.com/<xsl:value-of select="@id"/></xsl:variable>
            <xsl:if test="@picture">
                <tr>
                    <td align="center">
                        <a href="{$person_hyperlink}" target="_blank">
                            <xsl:variable name="picture_variable"><xsl:value-of select="@picture"/></xsl:variable>
                            <img src="{$picture_variable}"/>
                        </a>
                    </td>
                </tr>
            </xsl:if>
            <tr>
                <td align="center">
                    <font color="white">
                        <a href="{$person_hyperlink}" target="_blank"> <xsl:value-of select="@name"/></a>
                    </font>
                </td>
            </tr>
        </table>

    </xsl:template>

    <!-- attatchment template -->
    <xsl:template match="attatchment">

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

    <!--
    main templates
    -->

    <!-- stories template -->
    <xsl:template match="stories">

        <div class="w3-container w3-black w3-margin-bottom" align="center">

            <!-- Header of the story -->
            <h2>

                <table>
                    <col width="20%"/>
                    <col width="60%"/>
                    <col width="20%"/>
                    <tr>
                        <td align="center">
                            <!-- template for from -->
                            <xsl:apply-templates select="from"/>
                        </td>
                        <td align="center">
                            <xsl:if test="@story">
                                <font color="white">
                                    <xsl:value-of select="@story"/>
                                </font>
                            </xsl:if>
                        </td>
                        <td align="center">
                            <font color="white">
                                <xsl:value-of select="@created_time"/>
                            </font>
                        </td>
                    </tr>
                </table>

            </h2>

            <!-- body of the story -->
            <div class="w3-container w3-white">

                <!-- Image or Video -->
                <xsl:apply-templates select="attatchment"/>

                <br/>

                <!-- Message -->
                <xsl:value-of select="@message"/>

                <br/>

                <xsl:if test="comments">
                    <div class="w3-margin-top w3-container w3-blue" align="left">
                        <h4>Comentários</h4>

                        <!-- template for comments -->
                        <xsl:apply-templates select="comments"/>

                    </div>
                </xsl:if>

            </div>
        </div>

        <hr style="border: 1px solid #000" />

    </xsl:template>

    <!-- comments template -->
    <xsl:template match="comments">

        <div class="w3-container w3-blue">
            <table>
                <tr>
                    <td>
                        <font color="white">
                            &#9658;
                        </font>
                    </td>
                    <td>
                        <div class="w3-container w3-black">

                            <!-- Image or Video -->
                            <xsl:apply-templates select="attatchment"/>

                            <br/>

                            <table>
                                <col width="20%"/>
                                <col width="80%"/>
                                <tr>
                                    <table>
                                        <tr>
                                            <td align="center">
                                                <!-- template for from -->
                                                <xsl:apply-templates select="from"/>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <font color="white">
                                                    <xsl:value-of select="@created_time"/>
                                                </font>
                                            </td>
                                        </tr>
                                    </table>
                                    <td>
                                        <div class="w3-container w3-white">
                                            <xsl:value-of select="@message"/>
                                        </div>
                                    </td>
                                </tr>
                            </table>

                            <xsl:if test="reply">
                                <div class="w3-margin-top w3-container w3-margin-left w3-blue" align="left">
                                    <!-- template for reply -->
                                    <h4>Respostas</h4>
                                    <xsl:apply-templates select="reply"/>
                                </div>
                            </xsl:if>

                        </div>
                    </td>
                </tr>
            </table>
        </div>

    </xsl:template>

    <!-- reply template -->
    <xsl:template match="reply">

        <div class="w3-container w3-blue">

            <table>
                <tr>

                    <td>
                        <font color="white">
                            &#9711;
                        </font>
                    </td>

                    <td>
                        <div class="w3-container w3-black">

                            <!-- Image or Video -->
                            <xsl:apply-templates select="attatchment"/>

                            <br/>

                            <table>
                                <col width="20%"/>
                                <col width="80%"/>
                                <tr>
                                    <table>
                                        <tr>
                                            <td align="center">
                                                <!-- template for from -->
                                                <xsl:apply-templates select="from"/>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center">
                                                <font color="white">
                                                    <xsl:value-of select="@created_time"/>
                                                </font>
                                            </td>
                                        </tr>
                                    </table>
                                    <td>
                                        <div class="w3-container w3-white">
                                            <xsl:value-of select="@message"/>
                                        </div>
                                    </td>
                                </tr>
                            </table>

                        </div>
                    </td>
                </tr>
            </table>

        </div>

    </xsl:template>

</xsl:stylesheet>