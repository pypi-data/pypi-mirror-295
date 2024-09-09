/* global hljs */

$(document).ready(() => {
    'use strict';

    /**
     * Extend links to external website.
     * » add target="_blank"
     * » add rel="noopener noreferer"
     */
    const externalLinks = () => {
        const internalHost = [location.hostname];
        const protocolPattern = /^https?:\/\//i;

        /**
         * Walk through all links on the current page.
         */
        $('a').each((index, element) => {
            const href = $(element).attr('href');

            /**
             * Check if it's an HTTP link
             */
            if (protocolPattern.test(href)) {
                const hrefHostname = $(new URL(href)).attr('hostname');

                if ($.inArray(hrefHostname, internalHost) === -1) {
                    $(element).attr('target', '_blank');
                    $(element).attr('rel', 'noopener noreferer');
                }
            }
        });
    };


    /**
     * Render a JS clock for Eve time.
     *
     * @param {Element} element The HTML element to display the time
     */
    const renderClock = (element) => {
        const date = new Date();

        /**
         * Date
         * @type {string} 2021-01-01
         */
        // const year = date.getUTCFullYear();
        // const month = String(date.getUTCMonth() + 1).padStart(2, '0');
        // const day = String(date.getUTCDate()).padStart(2, '0');

        /**
         * Time
         * @type {string} 00:00:00
         */
        const hour = String(date.getUTCHours()).padStart(2, '0');
        const minute = String(date.getUTCMinutes()).padStart(2, '0');
        const second = String(date.getUTCSeconds()).padStart(2, '0');

        element.html(hour + ':' + minute + ':' + second);
    };


    /**
     * Check if an element has CSS overflow.
     *
     * @param {Element} element The element to check
     * @returns {{horizontal: boolean, overflow: boolean, vertical: boolean}}
     */
    const elementHasOverflow = (element) => {
        const clientHeight = element[0].clientHeight;
        const scrollHeight = element[0].scrollHeight;
        const clientWidth = element[0].clientWidth;
        const scrollWidth = element[0].scrollWidth;

        return {
            overflow: clientHeight < scrollHeight || clientWidth < scrollWidth,
            horizontal: clientWidth < scrollWidth,
            vertical: clientHeight < scrollHeight
        };
    };


    /**
     * Add classes to elements that have CSS overflow.
     *
     * @param {Element} element The element to check
     */
    const addOverflowClasses = (element) => {
        if (element.length > 0) {
            const {
                overflow, horizontal, vertical
            } = elementHasOverflow(element);

            if (overflow) {
                element.addClass('overflowing');

                if (vertical) {
                    element.addClass('overflowing-vertically');
                }

                if (horizontal) {
                    element.addClass('overflow-horizontally');
                }
            }
        }
    };


    /**
     * Functions that need to be executed on successful ajax events.
     */
    $(document).ajaxSuccess(() => {
        externalLinks();
    });


    /**
     * Functions that need to be executed when the page is loaded.
     */
    const init = () => {
        // Start the Eve-time clock in the top menu bar.
        setInterval(() => {
            renderClock($('.eve-time-wrapper .eve-time-clock'));
        }, 500);

        externalLinks();

        // It's not always loaded.
        if (typeof hljs !== 'undefined' && typeof hljs.highlightAll === 'function') {
            hljs.highlightAll();
        }

        // Add overflowing CSS classes to the Characters panel on the dashboard.
        addOverflowClasses(
            $('#aa-dashboard-panel-characters div.card-body > div:nth-child(2) > div')
        );

        // Add overflowing CSS classes to the Membership panel on the dashboard.
        addOverflowClasses(
            $('#aa-dashboard-panel-membership div.card-body > div:nth-child(2) > div')
        );
    };


    /**
     * Start the show
     */
    init();
});
