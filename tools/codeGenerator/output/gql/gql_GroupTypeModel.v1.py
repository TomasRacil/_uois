import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class GroupTypeModelEx(BaseModel):
    __tablename__ = 'grouptypes'
    __table_args__ = {'extend_existing': True} 
    
    groupmodels = relationship('GroupModelEx')
    # groupmodels = association_proxy('groupmodels', 'keyword')


class GroupTypeModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    
        
    groupmodels = graphene.List('graphqltypes.gql_GroupModel.GroupModel')
        
    def resolver_groupmodels(parent, info):
        return parent.groupmodels


class create_GroupTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_GroupTypeModel.GroupTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = GroupTypeModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_GroupTypeModel(ok=True, result=result)
    pass

class update_GroupTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_GroupTypeModel.GroupTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(GroupTypeModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_GroupTypeModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_grouptypes_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(GroupTypeModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_grouptypes_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(GroupTypeModelEx).filter(GroupTypeModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords