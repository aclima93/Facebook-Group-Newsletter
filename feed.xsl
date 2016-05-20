<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- Header and Footer -->
    <xsl:include href="header_footer.xsl"/>

    <xsl:template match="/">
        <html>

            <meta name="viewport" content="width=device-width, initial-scale=1"/>
            <link rel="stylesheet" href="http://www.w3schools.com/lib/w3.css"/>

            <body>

                <!-- Header -->
                <xsl:call-template name="header"/>

                <!-- Story Data -->
                <xsl:apply-templates select="objects/stories"/>

                <!-- Footer -->
                <xsl:call-template name="footer"/>

            </body>

        </html>
    </xsl:template>

    <xsl:template match="stories">

        <!-- Story -->
        <header class="w3-container w3-blue">
            <h2> <xsl:value-of select="@story"/> </h2>
        </header>
        <div class="w3-container w3-row-padding w3-margin">

            <!-- Message -->
            <div class="w3-third" align="center">
                <div class="w3-card-4">
                    <header class="w3-container w3-light-blue">
                        <h3>Nome</h3>
                    </header>
                    <div class="w3-container">
                        <p>
                            <xsl:value-of select="@message"/>
                        </p>
                    </div>
                </div>
            </div>

            <!-- Link -->
            <div class="w3-container w3-row-padding w3-margin">
                <div class="w3-card-4">

                    <xsl:variable name="hyperlink">https://www.facebook.com/<xsl:value-of select="@id"/></xsl:variable>
                    <div class="w3-container">
                        <p><xsl:value-of select="@summary_data" disable-output-escaping="no"/></p>
                        <div align="center">
                            <p><a href="{$hyperlink}" target="_blank">Link</a></p>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div class="w3-margin-top">
            <header class="w3-container w3-blue">
                <h2>Comentários</h2>
            </header>

            <!-- template for comments -->
            <xsl:apply-templates select="comments"/>

        </div>

    </xsl:template>

    <xsl:template match="comments">

        <table>

            <tr>
                <td>
                    <!-- template for from -->
                    <xsl:apply-templates select="from"/>
                </td>

                <td>
                    <b>
                        <xsl:value-of select="created_time"/>
                    </b>
                </td>
                <td>
                    <xsl:value-of select="message"/>
                </td>
            </tr>

            <tr>
                <!-- template for replies -->
                <xsl:apply-templates select="replies"/>
            </tr>

        </table>

    </xsl:template>

    <xsl:template match="from">

        <div class="w3-row-padding w3-margin">
            <div class="w3-card-4">

                <xsl:variable name="hyperlink">https://www.facebook.com/<xsl:value-of select="@id"/></xsl:variable>
                <header class="w3-container w3-light-blue">
                    <a href="{$hyperlink}" target="_blank"> <h4> <xsl:value-of select="name"/> </h4> </a>
                </header>

            </div>
        </div>

    </xsl:template>

    <xsl:template match="replies">

        <table>
            <tr>
                <td>
                    <!-- template for from -->
                    <xsl:apply-templates select="from"/>
                </td>

                <td>
                    <b>
                        <xsl:value-of select="created_time"/>
                    </b>
                </td>
                <td>
                    <xsl:value-of select="message"/>
                </td>
            </tr>
        </table>

    </xsl:template>

</xsl:stylesheet>