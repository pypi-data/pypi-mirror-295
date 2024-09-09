from django.db import models
from . import choices

# Create your models here.


class Address(models.Model):
    """A Person's Address"""

    area = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(default="NG", max_length=2, choices=choices.LOCATION_COUNTRIES)
    state = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    # Municipal, Local Government Area
    lga = models.CharField(max_length=255, blank=True, null=True)
    # Private Mail Box/ Post Office Box
    pmb = models.CharField(max_length=255, blank=True, null=True)
    typefk = models.IntegerField(default=1, choices=choices.LOCATION_TYPES)
    village = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        """Print version of Address"""

        address = ""
        fields = ["street", "area", "city", "lga", "zip_code", "state"]
        for field in fields:
            if field == "city" and getattr(self, "village"):
                field = "village"
            value = getattr(self, field)
            if value:
                address += f"{value.strip()}, "
        return address + self.get_country_display()

    class Meta:
        """Meta class for this Model"""

        abstract = True
        managed = True


class Email(models.Model):
    """A Person's Email Address"""

    email = models.EmailField(max_length=255, blank=True, null=True)
    typefk = models.IntegerField(default=1, choices=choices.LOCATION_TYPES)

    class Meta:
        """Meta class for this Model"""

        abstract = True
        managed = True


class Event(models.Model):
    """An event in a Person's Life"""

    authority = models.CharField(blank=True, null=True, max_length=255)
    end_date = models.DateField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    proof = models.IntegerField(default=0, choices=choices.EVENT_PROOFS)
    reference = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    typefk = models.IntegerField(default=0, choices=choices.EVENT_TYPES)

    class Meta:
        """Meta class for this Model"""

        abstract = True
        managed = True


class Group(models.Model):
    """Model of a Group of Persons"""

    about = models.CharField(blank=True, max_length=255, null=True)
    motto = models.CharField(blank=True, max_length=255, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        """Print String for this Model"""

        return self.name

    class Meta:
        """Meta class for this Model"""

        abstract = True
        managed = True


class MinimalAddress(models.Model):
    """A Person's Address"""

    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    typefk = models.IntegerField(default=1, choices=choices.LOCATION_TYPES)

    class Meta:
        """Meta class for this Model"""

        abstract = True
        managed = True


class MinimalContactPerson(models.Model):
    """Essentials for a Contact/Reference that is a Person"""

    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    job = models.IntegerField(default=0, blank=True, choices=choices.JOBS, null=True)    
    landmark = models.CharField(blank=True, null=True, max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(blank=True, null=True, max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    prefix = models.CharField(blank=True, choices=choices.HONORIFICS, null=True)
    suffix = models.CharField(blank=True, choices=choices.HONORIFICS, null=True)

    def __str__(self):
        """Print String for this Model"""

        return self.last_name

    @property
    def name(self):
        """Return the fullname of this Person"""

        prefix = self.prefix if self.prefix else ""
        middle_name = self.middle_name if self.middle_name else ""
        return f"{prefix} {self.last_name}, {self.first_name} {middle_name}"

    class Meta:
        """Meta class for this Model"""

        abstract = True
        managed = True


class MinimalPerson(models.Model):
    """Essentials for Person"""

    birthdate = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=255)
    job = models.IntegerField(default=0, blank=True, choices=choices.JOBS, null=True)
    last_name = models.CharField(max_length=255)
    marital_status = models.IntegerField(
        blank=True, choices=choices.MARITALSTATUS, null=True
    )
    middle_name = models.CharField(blank=True, null=True, max_length=255)
    nationality = models.CharField(
        default="NG", max_length=2, choices=choices.LOCATION_COUNTRIES
    )
    prefix = models.CharField(blank=True, choices=choices.HONORIFICS, null=True)
    sex = models.IntegerField(default=0, choices=choices.SEXES)
    suffix = models.CharField(blank=True, choices=choices.HONORIFICS, null=True)

    def __str__(self):
        """Print String for this Model"""

        return self.last_name

    @property
    def name(self):
        """Return the fullname of this Person"""

        prefix = self.prefix if self.prefix else ""
        middle_name = self.middle_name if self.middle_name else ""
        return f"{prefix} {self.last_name}, {self.first_name} {middle_name}"

    class Meta:
        """Meta class for this Model"""

        abstract = True
        managed = True


class Organization(models.Model):
    """A model of An Organization"""

    name = models.CharField(max_length=255)
    services = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255)
    motto = models.CharField(max_length=255)

    def __str__(self):
        """A text for identifying the Organization"""

        return self.name

    class Meta:
        """Meta class for Organization"""

        abstract = True
        managed = True


class Person(models.Model):
    """Model of a Person/Human"""

    blood_group = models.IntegerField(default=0, choices=choices.BLOODGROUPS)
    first_name = models.CharField(max_length=255)
    genotype = models.IntegerField(default=0, choices=choices.GENOTYPES)
    job = models.IntegerField(default=0, blank=True, choices=choices.JOBS, null=True)
    last_name = models.CharField(max_length=255)
    marital_status = models.IntegerField(
        blank=True, choices=choices.MARITALSTATUS, null=True
    )
    middle_name = models.CharField(blank=True, max_length=255, null=True)
    nationality = models.CharField(
        default="NG", max_length=2, choices=choices.LOCATION_COUNTRIES
    )
    nickname = models.CharField(blank=True, max_length=255, null=True)
    languages = models.CharField(blank=True, max_length=255, null=True)
    prefix = models.CharField(blank=True, choices=choices.HONORIFICS, null=True)
    religion = models.IntegerField(default=0, choices=choices.RELIGIONS)
    sex = models.IntegerField(default=0, choices=choices.SEXES)
    suffix = models.CharField(blank=True, choices=choices.HONORIFICS, null=True)

    def __str__(self):
        """Print String for this Model"""

        return self.last_name

    @property
    def name(self):
        """Return the fullname of this Person"""

        prefix = self.prefix if self.prefix else ""
        middle_name = self.middle_name if self.middle_name else ""
        return f"{prefix} {self.last_name}, {self.first_name} {middle_name}"

    class Meta:
        """Meta class for this Model"""

        abstract = True
        managed = True


class Phone(models.Model):
    """A Person's Phone Number"""

    number = models.CharField(max_length=255, blank=True, null=True)
    typefk = models.IntegerField(default=4, choices=choices.LOCATION_TYPES)

    class Meta:
        """Meta class for this Model"""

        abstract = True
        managed = True
