from odoo import models, fields
import os, PyPDF2
from odoo.exceptions import ValidationError
import base64
import re
from io import BytesIO
from pdfminer.high_level import extract_text
from unidecode import unidecode


class CreateCsf(models.TransientModel):
    _name = 'create.csf'
    _description = 'Create Csf'

    file = fields.Binary('Choose File')
    file_name = fields.Char()
    type = fields.Selection([('person', 'Individual'),
                             ('company', 'Company')], required=True)

    def create_csf(self):
        split_tup = os.path.splitext(self.file_name)
        file_extension = split_tup[1]
        if file_extension != '.pdf':
            raise ValidationError('Choose Valid File')
        else:
            country = self.env['res.country'].search([
                ('name', 'ilike', 'Mexico')])
            record = self.env['res.partner'].create({
                'name': ' ',
                'country_id': country.id,
            })
            if record:
                if self.type == 'person':
                    record.company_type = 'person'
                    attachment = self.env['ir.attachment'].create({
                        'name': self.file_name,
                        'type': 'binary',
                        'datas': self.file,
                        'res_model': record._name,
                        'res_id': record.id,
                        'mimetype': 'application/pdf'
                    })
                    record.message_post(body=self.file_name,
                                        attachment_ids=attachment.ids)
                    df_data = base64.b64decode(self.file)
                    pdf_data = BytesIO(df_data)
                    pdf_reader = PyPDF2.PdfFileReader(pdf_data)
                    textp = ''
                    text = extract_text(pdf_data)
                    # Define a regular expression to match the RFC value with 12 or 13 alphanumeric characters
                    rfc_regex = r'[A-Z]{3,4}\d{6}[A-Z0-9]{3,4}'

                    # Search for RFC values in the text using the regular expression
                    rfc_matches = re.findall(rfc_regex, text)

                    # Print the first RFC value found, if any
                    if rfc_matches:
                        rfc_value = rfc_matches[0]
                        if rfc_value:
                            record.vat = rfc_value

                    curp_regex = r'([A-Z0-9]{18})'

                    # Search for the CURP value in the text using the regular expression
                    curp_match = re.search(curp_regex, text)

                    # Check if a CURP value was found and print it
                    if curp_match:
                        curp_value = curp_match.group(1)
                        record.l10n_mx_edi_curp = curp_value

                    # Search for the Nombre value between "Registro Federal de Contribuyentes" and "Nombre, denominación o razón social"
                    nc_regex = r'Registro Federal de Contribuyentes\s*(.*?)\s*Nombre, denominación o razón\s*social'
                    nc_match = re.search(nc_regex, text)
                    if nc_match:
                        nc_value = nc_match.group(1).strip()
                        if nc_value:
                            record.name = nc_value
                    else:
                         nombre_regex = r'Registro Federal de Contribuyentes\s*(.*?)\s*Nombre, denominación o razón\s*social'
                         nombre_match = re.search(nombre_regex, text, re.DOTALL)
                         if nombre_match:
                             nc_value = nombre_match.group(1).strip().replace('\n', ' ')
                             record.name = nc_value

                    # Search for the Código Postal value
                    codigo_postal_regex = r'Código Postal:(\d{5})'
                    codigo_postal_match = re.search(codigo_postal_regex, text)
                    if codigo_postal_match:
                        codigo_postal_value = codigo_postal_match.group(
                            1).strip()
                        if codigo_postal_value:
                            record.zip = codigo_postal_value

                    # Search for the Tipo de Vialidad value in the text
                    tipo_vial_regex = r'Tipo de Vialidad: ([A-Z]+)'
                    tipo_vial_match = re.search(tipo_vial_regex, text)
                    if tipo_vial_match:
                        tipo_vial_value = tipo_vial_match.group(1)
                        if tipo_vial_value:
                            record.street_name = tipo_vial_value

                    # Search for the Número Exterior value in the text
                    num_ext_index = text.find("Número Exterior:")
                    if num_ext_index != -1:
                        num_ext_value = \
                            text[
                            num_ext_index + len("Número Exterior:"):].split(
                                "\n")[0].strip()
                        if num_ext_index:
                            record.street_number = num_ext_value

                    # Search for the Número Interior value in the text
                    num_int_index = text.find("Número Interior:")
                    if num_int_index != -1:
                        num_int_value = text[num_int_index + len(
                            "Número Interior:"):].strip().split("\n")[0]
                        if num_int_value.startswith("Nombre de la Colonia"):
                            num_int_value = ""
                        if num_int_value:
                            record.street_number2 = num_int_value

                    # Search for the Nombre de Vialidad value in the text
                    nv_index = text.find("Nombre de Vialidad:")
                    if nv_index != -1:
                        nv_value = \
                            text[nv_index + len("Nombre de Vialidad:"):].split(
                                "\n")[0].strip()
                        if nv_value:
                            record.street_name = nv_value

                    # Search for the Nombre de la Colonia value in the text
                    col_index = text.find("Nombre de la Colonia:")
                    if col_index != -1:
                        col_value = \
                            text[
                            col_index + len("Nombre de la Colonia:"):].split(
                                "\n")[0].strip()
                        if col_value:
                            record.l10n_mx_edi_colony = col_value

                    country = self.env['res.country'].search([
                        ('name', '=', 'México')])

                    # Search for the Nombre de la Entidad Federativa value in the text
                    entidad_index = text.find("Nombre de la Entidad Federativa:")
                    if entidad_index != -1:
                        entidad_value = text[entidad_index + len(
                            "Nombre de la Entidad Federativa:"):].strip().split(
                            "\n")[0]
                        if entidad_value:
                            if entidad_value == 'MEXICO':
                                state = self.env['res.country.state'].search([
                                    ('name', '=', 'México'),
                                    ('country_id', '=', country.id)],
                                    limit=1)
                                record.state_id = state.id
                            else:
                                state = self.env['res.country.state'].search([
                                    ('name', 'like', entidad_value.title()),
                                    ('country_id', '=', country.id)],
                                    limit=1)
                                record.state_id = state.id    
                            
                            
                    # Search for the Nombre del Municipio o Demarcación Territorial value in the text
                    municipio_index = text.find(
                        "Nombre del Municipio o Demarcación Territorial:")
                    if municipio_index != -1:
                        municipio_value = text[municipio_index + len(
                            "Nombre del Municipio o Demarcación Territorial:"):].strip().split(
                            "\n")[0]
                    if municipio_value:
                        city = self.env['res.city'].search([
                            ('name', 'like', municipio_value.title()),
                            ('state_id', '=', state.id)], limit=1)
                        record.city_id = city.id
                    for i in range(pdf_reader.getNumPages()):
                        page = pdf_reader.getPage(i)
                        textp += page.extractText()
                    regimen_matches = re.findall(r'Régimen de[^\r\n]*(?=Obligaciones:)', textp)
                    for regimen in regimen_matches:
                        regex = r'\d{2}/\d{2}/\d{4}'
                        matches = re.findall(regex, regimen)
                        result = re.split(regex, regimen)
                        result = [r.strip() for r in result if r.strip()]
                        message = str(result)
                    return {
                        'warning': {'title': 'Favor de elegir el regimen correcto',
                                            'message': message}
                    #   ,
                    #    'type': 'ir.actions.act_window',
                    #    'target': 'current',
                    #    'view_mode': 'form',
                    #    'res_model': 'res.partner',
                    #    'res_id': record.id,
                    }
                
        return super(CreateCsf, self)
                elif self.type == 'company':
                    record.company_type = 'company'
                    attachment = self.env['ir.attachment'].create({
                        'name': self.file_name,
                        'type': 'binary',
                        'datas': self.file,
                        'res_model': record._name,
                        'res_id': record.id,
                        'mimetype': 'application/pdf'
                    })
                    record.message_post(body=self.file_name,
                                        attachment_ids=attachment.ids)
                    df_data = base64.b64decode(self.file)
                    pdf_data = BytesIO(df_data)
                    text = extract_text(pdf_data)
                    rfc_regex = r'[A-Z]{3,4}\d{6}[A-Z0-9]{3,4}'

                    # Search for RFC values in the text using the regular expression
                    rfc_matches = re.findall(rfc_regex, text)

                    # Print the first RFC value found, if any
                    if rfc_matches:
                        rfc_value = rfc_matches[0]
                        if rfc_value:
                            record.vat = rfc_value

                    # Search for the Denominación/Razón Social value in the text
                    razon_social_index = text.find(
                        "Denominación/Razón Social:")
                    if razon_social_index != -1:
                        razon_social_value = text[razon_social_index + len(
                            "Denominación/Razón Social:"):].strip().split(
                            "\n")[0]
                        if razon_social_value:
                            record.name = razon_social_value

                    # Search for the Régimen Capital value in the text
                    regimen_index = text.find("Régimen Capital:")
                    if regimen_index != -1:
                        regimen_value = text[regimen_index + len(
                            "Régimen Capital:"):].strip().split("\n")[0]

                    # Search for the Código Postal value in the text
                    cp_index = text.find("Código Postal:")
                    if cp_index != -1:
                        cp_value = \
                            text[
                            cp_index + len("Código Postal:"):].strip().split(
                                "\n")[0]
                        if cp_value:
                            record.zip = cp_value

                    # Search for the Nombre de Vialidad value in the text
                    vialidad_index = text.find("Nombre de Vialidad:")
                    if vialidad_index != -1:
                        vialidad_value = text[vialidad_index + len(
                            "Nombre de Vialidad:"):].strip().split("\n")[0]
                        if vialidad_value:
                            record.street_name = vialidad_value

                    # Search for the Número Exterior value in the text
                    num_ext_index = text.find("Número Exterior:")
                    if num_ext_index != -1:
                        num_ext_value = text[num_ext_index + len(
                            "Número Exterior:"):].strip().split("\n")[0]
                        if num_ext_value:
                            record.street_number = num_ext_value

                    # Search for the Número Interior value in the text
                    num_int_index = text.find("Número Interior:")
                    if num_int_index != -1:
                        num_int_value = text[num_int_index + len(
                            "Número Interior:"):].strip().split("\n")[0]
                        if num_int_value.startswith("Nombre de la Colonia"):
                            num_int_value = ""
                        if num_int_value:
                            record.street_number2 = num_int_value

                    # Search for the Nombre de la Colonia value in the text
                    colonia_index = text.find("Nombre de la Colonia:")
                    if colonia_index != -1:
                        colonia_value = text[colonia_index + len(
                            "Nombre de la Colonia:"):].strip().split("\n")[0]
                        if colonia_value:
                            record.l10n_mx_edi_colony = colonia_value

                    country = self.env['res.country'].search([
                        ('name', '=', 'México')])

     
                    # Search for the Nombre de la Entidad Federativa value in the text
                    entidad_index = text.find("Nombre de la Entidad Federativa:")
                    if entidad_index != -1:
                        entidad_value = text[entidad_index + len(
                            "Nombre de la Entidad Federativa:"):].strip().split(
                            "\n")[0]
                        if entidad_value:
                            if entidad_value == 'MEXICO':
                                state = self.env['res.country.state'].search([
                                    ('name', '=', 'México'),
                                    ('country_id', '=', country.id)],
                                    limit=1)
                                record.state_id = state.id
                            else:
                                state = self.env['res.country.state'].search([
                                    ('name', 'like', entidad_value.title()),
                                    ('country_id', '=', country.id)],
                                    limit=1)
                                record.state_id = state.id    
                            
                            
                    # Search for the Nombre del Municipio o Demarcación Territorial value in the text
                    municipio_index = text.find(
                        "Nombre del Municipio o Demarcación Territorial:")
                    if municipio_index != -1:
                        municipio_value = text[municipio_index + len(
                            "Nombre del Municipio o Demarcación Territorial:"):].strip().split(
                            "\n")[0]
                    if municipio_value:
                        city = self.env['res.city'].search([
                            ('name', 'like', municipio_value.title()),
                            ('state_id', '=', state.id)], limit=1)
                        record.city_id = city.id

                    # Search for the Régimen General de Ley Personas Morales value in the text
                    regimen_regex = r"Régimen General de Ley Personas Morales"
                    regimen_match = re.search(regimen_regex, text)
                    if regimen_match:
                        regimen_value = regimen_match.group().strip()
                        regimen_value = regimen_value.replace("Régimen ", "")
                        # if regimen_value:
                        #     record.l10n_mx_edi_fiscal_regime = regimen_value

                    return {
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'view_mode': 'form',
                        'res_model': 'res.partner',
                        'res_id': record.id,
                    }

