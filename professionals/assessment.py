from django.contrib.auth import get_user_model
from django.db.models import Avg

User = get_user_model()

def ass_query(obj):
    query = User.objects.exclude(is_headhunter=True)
    query = query.filter(score__rank=obj.score.rank)
    # query = query.filter(state=obj.state)
    query = query.filter(
        professional__main_module=obj.professional.main_module
    )
    return query

def get_average(query, atribute):
    return query.aggregate(Avg(f'professional__{atribute}'))

def variation(variation, query):
    x = 100 * variation / query.count()
    x = round(x, 2)
    return x

def get_value(average):
    x = list(average.values())[0]
    if x == None or x == 0:
        x = 0
    return x

def working_years_context(obj, q):
    context = dict()
    if obj.professional.working_years != 0:
        kwargs = {f'professional__working_years__lte': obj.professional.working_years}
        average_field = get_average(q, 'working_years')
        avg_field_name = f'professional__working_years__avg'
        context[f'average_working_years'] = average_field
        wy_outliers = q.filter(**kwargs)
        wy_outliers = wy_outliers.count()
        context['working_years_variation'] = variation(wy_outliers, q)

    return context

def implementations_context(obj, q):
    context = dict()
    if obj.professional.implementations != 0:
        kwargs = {f'professional__implementations__lte': obj.professional.implementations}
        average_field = get_average(q, 'implementations')
        avg_field_name = f'professional__implementations__avg'
        context[f'average_implementations'] = average_field
        wy_outliers = q.filter(**kwargs)
        wy_outliers = wy_outliers.count()
        context['implementations_variation'] = variation(wy_outliers, q)

    return context

def supports_context(obj, q):
    context = dict()
    if obj.professional.supports != 0:
        kwargs = {f'professional__supports__lte': obj.professional.supports}
        average_field = get_average(q, 'supports')
        avg_field_name = f'professional__supports__avg'
        context[f'average_supports'] = average_field
        wy_outliers = q.filter(**kwargs)
        wy_outliers = wy_outliers.count()
        context['supports_variation'] = variation(wy_outliers, q)

    return context

# def get_context_integerfields(obj, q):
#     context = dict()
#     query = q

#     obj_fields = {
#         # obj.professional.working_years: 'working_years',
#         obj.professional.implementations: 'implementations',
#         obj.professional.supports: 'supports',
#     }

#     for field in obj_fields.keys():
#         if field != 0:
#             kwargs = {f'professional__{obj_fields[field]}__lte': field}
#             average_field = get_average(query, obj_fields[field])
#             avg_field_name = f'professional__{obj_fields[field]}__avg'
#             context[f'average_{obj_fields[field]}'] = average_field
#             wy_outliers = query.filter(**kwargs)
#             wy_outliers = wy_outliers.count()
#             context[obj_fields[field] + '_variation'] = variation(wy_outliers, query)

#     return context

def get_context_listfields(obj, q):
    context = dict()
    query = q

    if obj.professional.len_modules:
        if obj.professional.len_modules == 1:
            kwargs = {'professional__secondary_module': None}
            len_modules_outliers = len(query.exclude(**kwargs))
        elif obj.professional.len_modules == 2:
            kwargs = {'professional__terciary_module': None}
            len_modules_outliers = len(query.exclude(**kwargs))
        elif obj.professional.len_modules == 3:
            kwargs = {'professional__len_modules': obj.professional.len_modules}
            len_modules_outliers = len(query.filter(**kwargs))
        context['len_modules_variation'] = variation(
            len_modules_outliers, query
        )
    else:
        context['len_modules_variation'] = 0
    return context

def get_context_industries(obj, q):
    context = dict()
    query = q

    if obj.professional.len_industries:
        if obj.professional.len_industries == 1:
            kwargs = {'professional__secondary_industry': None}
            len_industries_outliers = len(query.exclude(**kwargs))
        elif obj.professional.len_industries == 2:
            kwargs = {'professional__terciary_industry': None}
            len_industries_outliers = len(query.exclude(**kwargs))
        elif obj.professional.len_industries == 3:
            kwargs = {'professional__len_industries': obj.professional.len_industries}
            len_industries_outliers = len(query.filter(**kwargs))
        context['len_industries_variation'] = variation(
            len_industries_outliers, query
        )
    else:
        context['len_industries_variation'] = 0
    return context

def get_context_methodology(obj, q):
    context = dict()
    query = q
    query_activate = len(query.filter(professional__methodology='ACTIVATE'))

    context['methodology_activate'] = variation(query_activate, query)
    return context

def ass_methodology(methodology):
    if methodology == 'ACTIVATE':
        mensagem = """Quanto ao conhecimento de metodologia, parab??ns! 
        Voc?? j?? conhece a SAP Activate e est?? na frente da maioria dos 
        profissionais de mercado mas, 
        continue se atualizando pois, esta nova Abordagem 
        ser?? a base para todos os projetos daqui para frente.
        """
    else:
        mensagem = """Quanto ao conhecimento de metodologia, 
        voc?? precisa se atualizar! 
        A SAP lan??ou um nova Abordagem chamada de SAP Activate 
        que ser?? a base para todos os projetos daqui para frente. 
        """
    return mensagem

def ass_modules(context):
    if  context['len_modules_variation'] >= 50:
        mensagem = """
            Tamb??m ?? importante mencionar que os profissionais com seu perfil
             conhecem mais m??dulos ou solu????es SAP que voc??.
            Vale a pena avaliar as solu????es SAP mais alinhadas com o processo 
            de neg??cio que voc?? ?? especialista e identificar se existe alguma
             oportunidade que ir?? melhorar sua empregabilidade.
        """
    else:
        mensagem = """
            Parab??ns, seu conhecimento t??cnico est?? alinhado com o que o 
            mercado espera de profissionais com o seu perfil.
        """
    return mensagem

def ass_industries(context):
    if  context['len_industries_variation'] >= 50:
        mensagem = """
            Avalie solu????es de ind??stria alinhadas a sua experi??ncia 
            profissional que podem trazer um diferencial de mercado.
        """
    else:
        mensagem = """
            Seu conhecimento das ind??stria podem ser  um diferencial 
            profissional. Avalie a demanda do mercado para a solu????o que voc?? 
            conhece,  e se n??o houver uma demanda relevante avalie outras 
            solu????es que possam melhorar sua empregabilidade.
        """
    return mensagem

def ass_main(
        working_years, 
        wy_avg, 
        implementations, 
        implementations_avg, 
        supports,
        supports_avg):
    context = dict()

    if (
        working_years > wy_avg and 
        implementations > implementations_avg and
        supports > supports_avg):
            mensagem = """A maioria dos profissionais com seu perfil, 
            tem mais tempo de experi??ncia 
            em SAP e j?? trabalharam em mais projetos de implanta????o e 
            opera????es de suporte.
            Se voc?? puder priorizar os projetos de implanta????o, eles s??o mais 
            reconhecidos pelos contratantes e ir??o ajudar a tornar seu 
            curr??culo 
            mais atrativo. Assim, voc?? pode compensar o menor 
            tempo de experi??ncia 
            em rela????o a m??dia do mercado.
            """
    elif (
        wy_avg > working_years and
        implementations_avg > implementations and
        supports_avg > supports):
            mensagem = """A maioria dos profissionais com seu perfil, tem mais 
            tempo de experi??ncia em SAP que voc??.
            Mas, o n??mero de implanta????es que voc?? j?? participou ?? muito bom. 
            Os projetos de implanta????o s??o mais reconhecidos pelos 
            contratantes e ir??o ajudar a tornar seu curr??culo mais atrativo. 
            Assim, voc?? pode compensar o menor tempo de experi??ncia em rela????o 
            a m??dia do mercado.
            """
    elif (
        wy_avg > working_years and
        implementations_avg > implementations and
        supports_avg <= supports):
            mensagem = """A maioria dos profissionais com seu perfil, tem mais 
            tempo de experi??ncia em SAP que voc??.
            As opera????es de suporte s??o uma boa oportunidade para voc?? 
            adquirir conhecimento sobre os m??dulos e solu????es SAP.
            Mas, se voc?? conseguir trabalhar em mais projetos de implanta????o 
            ser?? bem interessante. 
            Os projetos de implanta????o s??o mais reconhecidos pelos 
            contratantes e ir??o ajudar a tornar seu curr??culo mais atrativo. 
            Assim, voc?? pode compensar o menor tempo de experi??ncia em rela????o 
            a m??dia do mercado.
            """
    elif (
        wy_avg > working_years and
        implementations_avg <= implementations and
        supports_avg <= supports):
            mensagem = """A maioria dos profissionais com seu perfil, tem mais 
            tempo de experi??ncia em SAP que voc??.
            Mas, o n??mero de implanta????es que voc?? j?? participou ?? muito bom. 
            Os projetos de implanta????o s??o mais reconhecidos pelos 
            contratantes e ir??o ajudar a tornar seu curr??culo mais atrativo. 
            Assim, voc?? pode compensar o menor tempo de experi??ncia em 
            rela????o a m??dia do mercado.
            """
    elif (
        wy_avg <= working_years and
        implementations_avg > implementations and
        supports_avg > supports):
            mensagem = """Seu tempo de experi??ncia em SAP ?? bom para seu 
            perfil, mas seria bom se voc?? conseguisse trabalhar em mais 
            projetos de implanta????o.
            Os projetos de implanta????o s??o mais reconhecidos pelos contratantes 
            e ir??o ajudar a tornar seu curr??culo mais atrativo.
            """
    elif (
        wy_avg <= working_years and
        implementations_avg <= implementations and
        supports_avg > supports):
            mensagem = """Seu tempo de experi??ncia em SAP ?? bom para seu perfil.
            Quanto mais projeto de implanta????o voc?? participar melhor.
            Os projetos de implanta????o s??o mais reconhecidos pelos contratantes e ir??o 
            ajudar a tornar seu curr??culo mais atrativo.
            """
    elif (
        wy_avg <= working_years and
        implementations_avg > implementations and
        supports_avg <= supports):
            mensagem = """Seu tempo de experi??ncia em SAP ?? bom para seu perfil, 
            mas seria bom se voc?? conseguisse trabalhar em mais projetos de implanta????o.
            As opera????es de suporte s??o uma boa oportunidade para voc?? 
            adquirir conhecimento sobre os m??dulos e solu????es SAP.
            Mas, se voc?? conseguir trabalhar em mais projetos de implanta????o 
            ser?? bem interessante. 
            Os projetos de implanta????o s??o mais reconhecidos pelos 
            contratantes e ir??o ajudar a tornar seu curr??culo mais atrativo. 
            """
    elif (
        wy_avg <= working_years and
        implementations_avg <= implementations and
        supports_avg <= supports):    
            mensagem = """Seu tempo de experi??ncia em SAP ?? bom para seu perfil.
            Quanto mais projeto de implanta????o voc?? participar melhor.
            Os projetos de implanta????o s??o mais reconhecidos pelos contratantes e ir??o 
            ajudar a tornar seu curr??culo mais atrativo.
            """

    context['ass_main'] = mensagem
    return mensagem

def assessment(obj):
    query = ass_query(obj)
    context = dict()
    context.update(implementations_context(obj, query))
    context.update(working_years_context(obj, query))
    context.update(supports_context(obj, query))
    context.update(get_context_listfields(obj, query))
    context.update(get_context_industries(obj, query))
    context.update(get_context_methodology(obj, query))
    context['ass_main'] = ass_main(
            working_years=obj.professional.working_years,
            wy_avg=list(query.aggregate(Avg(f'professional__working_years')).values())[0],
            implementations=obj.professional.implementations,
            implementations_avg=list(query.aggregate(Avg(f'professional__implementations')).values())[0],
            supports=obj.professional.supports,
            supports_avg=list(query.aggregate(Avg(f'professional__supports')).values())[0],
        )
    context['ass_methodology'] = ass_methodology(obj.professional.methodology)
    context['ass_modules'] = ass_modules(context)
    context['ass_industries'] = ass_industries(context)
    return context