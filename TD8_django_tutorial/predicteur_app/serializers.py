from rest_framework import serializers
from predicteur_app.models import House


class HouseSerializer(serializers.Serializer)  :
    """ to serialize or deserialize data
    -> Serialize                               : model instance / querysets => native Python datatypes => JSON
        ** NETWORK **
    -> Deserialize                             : JSON to model instance
    """

    CRIM    = serializers.FloatField()
    ZN      = serializers.FloatField()
    INDUS   = serializers.FloatField()
    CHAS    = serializers.FloatField()
    NOX     = serializers.FloatField()
    RM      = serializers.FloatField()
    AGE     = serializers.FloatField()
    DIS     = serializers.FloatField()
    RAD     = serializers.FloatField()
    TAX     = serializers.FloatField()
    PTRATIO = serializers.FloatField()
    B       = serializers.FloatField()
    LSTAT   = serializers.FloatField()
    MEDV    = serializers.FloatField(allow_null=True)

    def create(self, validated_data)           :
        """ Create and return a new 'House' instance, given the validated data """
        return House.objects.create(**validated_data)

    def update(self, instance, validated_data) :
        """ Update and return an existing 'Houste' instance, given the validated data """
        instance.CRIM    = validated_data.get('CRIM' , instance.CRIM)
        instance.ZN      = validated_data.get('ZN' , instance.ZN)
        instance.INDUS   = validated_data.get('INDUS' , instance.INDUS)
        instance.CHAS    = validated_data.get('CHAS' , instance.CHAS)
        instance.NOX     = validated_data.get('NOX' , instance.NOX)
        instance.RM      = validated_data.get('RM' , instance.RM)
        instance.AGE     = validated_data.get('AGE' , instance.AGE)
        instance.DIS     = validated_data.get('DIS' , instance.DIS)
        instance.RAD     = validated_data.get('RAD' , instance.RAD)
        instance.TAX     = validated_data.get('TAX' , instance.TAX)
        instance.PTRATIO = validated_data.get('PTRATIO' , instance.PTRATIO)
        instance.B       = validated_data.get('B' , instance.B)
        instance.LSTAT   = validated_data.get('LSTAT' , instance.LSTAT)
        #instance.MEDV   = validated_data.get('MEDV' , instance.MEDV)
        instance.save()
        return instance
