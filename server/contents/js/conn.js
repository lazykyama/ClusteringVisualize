/**
 * conn.js
 * @auther kyama http://sukimaprogrammer.blogspot.jp/
 * @since 0.0.1
 * @version 0.0.1
 * 
 * This source is distributed under the MIT License.
 * 
 * Copyright (c) 2013 kyama http://sukimaprogrammer.blogspot.jp/
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

// require jQuery

// definition.
kyama.conn = kyama.conn || {};

/**
 * update sample dataset and cluster assigns via server.
 * @param params request parameters object.
 *        params.sessionid session ID to identify the request. (optional)
 *        params.step the kmeans learning step. (optional)
 *        params.size the sample size.
 *        params.k the cluster size.
 * @param successFn callback method on success.
 *        successFn(json)
 * @param errorFn callback method on error.
 *        errorFn(xhr, textStatus, errorThrown)
 * @param completeFn callback method on complete.
 */
kyama.conn.update = function(params, successFn, errorFn, completeFn) {
    // request.
    var url = window.location.pathname.split('/contents/')[0] + '/rest/kmeans_result';
    
    $.ajax({
	type : 'GET',
	url : url,
	data : params,
	cache : false
    })
    .done(successFn)
    .fail(errorFn)
    .always(completeFn);
};
