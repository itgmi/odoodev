# from odoo import http
#
#
# class ImageUrl(http.Controller):
#     @http.route(['/product/images/<int:id>'],
#                 type='http', auth="public")
#     # pylint: disable=redefined-builtin,invalid-name
#     def content_image(self, xmlid=None, model='ir.attachment', id=None,
#                       field='raw',
#                       filename_field='name', filename=None, mimetype=None,
#                       unique=False,
#                       download=False, width=0, height=0, crop=False,
#                       access_token=None,
#                       nocache=False):
#         try:
#             record = request.env['ir.binary']._find_record(xmlid, model,
#                                                            id and int(id),
#                                                            access_token)
#             stream = request.env['ir.binary']._get_image_stream_from(
#                 record, field, filename=filename,
#                 filename_field=filename_field,
#                 mimetype=mimetype, width=int(width), height=int(height),
#                 crop=crop,
#             )
#         except UserError as exc:
#             if download:
#                 raise request.not_found() from exc
#             # Use the ratio of the requested field_name instead of "raw"
#             if (int(width), int(height)) == (0, 0):
#                 width, height = image_guess_size_from_field_name(field)
#             record = request.env.ref('web.image_placeholder').sudo()
#             stream = request.env['ir.binary']._get_image_stream_from(
#                 record, 'raw', width=int(width), height=int(height), crop=crop,
#             )
#
#         send_file_kwargs = {'as_attachment': download}
#         if unique:
#             send_file_kwargs['immutable'] = True
#             send_file_kwargs['max_age'] = http.STATIC_CACHE_LONG
#         if nocache:
#             send_file_kwargs['max_age'] = None
#
#         return stream.get_response(**send_file_kwargs)