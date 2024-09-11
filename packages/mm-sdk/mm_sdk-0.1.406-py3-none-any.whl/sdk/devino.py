from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, Json

from .client import Empty, HttpUrl, SDKClient, SDKResponse


class AddressBookSource(BaseModel):
    addressBookSourceType: str  # Тип адресной книги, используется для фильтра (BIRTHDAY, PERIODIC, SIMPLE)
    byOptimalSendTime: Optional[bool]  # Персонализированное время отправки
    byTimeZone: Optional[bool]  # Учет местного времени контакта при отправке
    checkDuplicate: Optional[bool]  # Проверка дубликатов контактов в адресной книге
    contactCountId: Optional[int]  # ID количества контактов в адресной книге
    contactGroupIds: List[
        int
    ]  # Массив ID групп контактов в адресной книге. Не используется вместе с параметром segmentIds
    stopContactGroupIds: Optional[List[int]]  # Массив ID стоп-листов контактов
    period: Optional[str]  # Периодичность (ONCE, DAILY, WEEKLY, MONTHLY)
    segmentIds: Optional[
        List[int]
    ]  # Массив ID сегментов внутри групп контактов адресной книги, если группа контактов разделена на сегменты
    smoothSendMinutes: Optional[
        int
    ]  # Плавная отправка, задается в минутах (от 0 до 1440)


class TaskInfo(BaseModel):
    scenarioType: Optional[str]  # Тип сценария. Используется при "type": "EVENT_FLOW"


class EventSources(BaseModel):
    channel: Optional[
        str
    ]  # Канал триггера (EMAIL, FLASHCALL, HLR, PUSH, PUSH_WALLET, SMS, VIBER, VK, VOICE, WHATSAPP)
    eventType: str  # Тип события (CONTACT_MOBILE_EVENT, CONTACT_WEB_EVENT, STATE)
    eventValue: Optional[str]  # События, при которых совершается рассылка


class EventCollectorSettings(BaseModel):
    maxNewRegisterSec: Optional[
        int
    ]  # Время после совершения события в секундах, в течение которого рассылка не будет повторяться
    onlyUpdateEventSources: Optional[
        List[EventSources]
    ]  # Массив событий для совершения повторяющихся рассылок


class GeoSettings(BaseModel):
    antiFraudMins: Optional[int]  # Время в минутах для повторной отправки сообщения
    locationIds: Optional[List[int]]  # Массив ID геолокаций
    pushApplicationIds: Optional[
        List[int]
    ]  # Массив ID приложений, в которых будет проведена рассылка


class NoEventSourceSettings(BaseModel):
    # не указано в доке
    pass


class Template(BaseModel):
    pass


class SmsTemplate(Template, BaseModel):
    shortenUrl: Optional[bool]  # При true сокращает длину ссылок в тексте сообщения
    from_alias: str = Field(alias="from")  # Согласованное имя отправителя
    text: str  # Текст сообщения (до 17085 символов включительно при использовании кириллицы)
    validity: int  # Срок жизни сообщения в секундах (по умолчанию 0, от 0 до 3 суток)


class EmailTemplate(Template, BaseModel):
    sourceAddress: str  # Email-адрес отправителя
    sourceName: str  # Имя отправителя
    subject: str  # Тема письма
    htmlBody: str  # Тело письма в формате HTML
    plainText: Optional[
        str
    ]  # Тело письма в формате Plaintext, все теги отображаются как обычный текст
    attachmentIds: Optional[List[int]]  # Массив файлов, прикрепленных к письму


class VkTemplate(Template, BaseModel):
    routes: List[str]  # Список возможных каналов доставки через запятую ([VK, OK])
    deliveryPolicy: Optional[
        str
    ]  # По умолчанию any. Возможные значения: any, mobile_device_required, verified_phone_number
    validity: Optional[
        int
    ]  # Срок жизни сообщения в секундах. (от 60 до 86400 (по умолчанию))
    templateId: str  # ID шаблона сообщения в Devino
    templateData: Optional[Json]  # JSON-объект, где ключи - имена переменных в шаблоне
    callbackData: Optional[
        str
    ]  # Данные, которые будут указаны в коллбэке со статусом сообщения
    callbackUrl: Optional[
        str
    ]  # URL, на который система будет отправлять коллбэки при изменении статуса сообщения


class WhatsAppTemplate(Template, BaseModel):
    pass


class ViberTemplate(Template, BaseModel):
    from_alias: str = Field(
        alias="from"
    )  # Имя отправителя, которое используется при отправке сообщения.
    action: Optional[
        str
    ]  # URL или deep link, на который перейдет пользователь после нажатия на кнопку
    caption: Optional[str]  # Текст кнопки, не более 30 символов в кодировке UTF-
    image: Optional[str]  # URL изображения в форматах JPG, JPEG или PNG
    text: Optional[str]  # Текст сообщения в кодировке UTF-8
    validity: Optional[int]  # Срок жизни сообщения в секундах


class PushTemplate(Template, BaseModel):
    pass


class PushWalletTemplate(Template, BaseModel):
    pass


class Templates(BaseModel):
    smsTemplate: Optional[SmsTemplate]
    viberTemplate: Optional[ViberTemplate]
    emailTemplate: Optional[EmailTemplate]
    pushTemplate: Optional[PushTemplate]
    pushWalletTemplate: Optional[PushWalletTemplate]
    whatsAppTemplate: Optional[WhatsAppTemplate]
    vkTemplate: Optional[VkTemplate]


class Triggers(BaseModel):
    channel: str  # Канал триггера (EMAIL, FLASHCALL, HLR, PUSH, PUSH_WALLET, SMS, VIBER, VK, VOICE, WHATSAPP)
    type: str  # Тип триггера (ADDRESS_BOOK_SOURCE, TRAN_API_SOURCE, EVENT_SOURCE, NO_EVENT_SOURCE, EVENT_COLLECTOR, GEO_LOCATION)
    index: int  # ID триггера
    parentIndex: Optional[int]  # ID родительского триггера
    startTime: Optional[datetime]  # Дата старта триггера. Формат - YYYY-MM-DD hh:mm:ss
    endTime: Optional[datetime]  # Дата окончания триггера. Формат - YYYY-MM-DD hh:mm:ss
    eventSources: Optional[List[EventSources]]  # Массив событий для совершения рассылок
    eventCollectorSettings: Optional[
        EventCollectorSettings
    ]  # Параметры повторяющихся рассылок по событиям
    geoSettings: Optional[GeoSettings]  # Параметры гео-рассылок
    noEventSourceSettings: Optional[
        NoEventSourceSettings
    ]  # Содержит параметр: stateWaitMaxTimeSec (integer) - время ожидания события в секундах
    template: Optional[Templates]  # Массив шаблонов сообщений


class CreateOmniTaskRequest(BaseModel):
    addressBookSource: Optional[AddressBookSource]  # Параметры адресных книг
    channel: str  # Канал рассылки: EMAIL, OMNI, PUSH, SMS, VIBER, VK, WHATSAPP
    draftId: Optional[int]  # ID черновика рассылки
    taskInfo: Optional[TaskInfo]  # Тип сценария, который активирует триггерную рассылку
    taskName: str  # Название рассылки. От 1 до 100 символов
    triggers: List[Triggers]  # Параметры триггеров dict
    type: str  # Тип рассылки (SIMPLE - одноразовая рассылка)


class Fields(BaseModel):
    pass


class PushInfo(BaseModel):
    pass


class Contact(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    pushInfo: Optional[List[PushInfo]]  # Данные push-уведомления.
    fields: Optional[List[Fields]]  # Параметры макросов (полей) контактов в списке


class Contacts(BaseModel):
    contact: Contact
    callbackUrl: Optional[str]
    callbackData: Optional[Dict]


class SendTransactionalMessageRequest(BaseModel):
    taskId: int  # ID сценария рассылки
    contactIds: Optional[List[str]]  # ID контактов из адресных книг
    contacts: Optional[List[Contacts]]
    templates: Optional[Dict[str, Template]]


class SendAnswers(BaseModel):
    code: str
    mergeKey: str
    result: str
    reasons: List[Dict]


class ErrorAnswers(BaseModel):
    code: str
    result: str
    description: str
    reasons: List[Dict]


class SendTransactionalMessageResponse(BaseModel):
    contactIds: List[str]  # Массив ID загруженных контактов
    sendAnswers: List[SendAnswers]  # Массив успешно отправленных сообщений
    errorAnswers: List[ErrorAnswers]  # Массив неуспешно отправленных сообщений


class DevinoService:
    def __init__(self, client: SDKClient, url: HttpUrl, token: str):
        self._client = client
        self._url = url
        self._token = token
        self.create_omni_scenario_url = self._url + "omni-task-api/tasks/"
        self.send_transactional_message_url = self._url + "omni-scheduler/api/messages/"

    def create_omni_scenario(
        self, query: CreateOmniTaskRequest, timeout=3
    ) -> SDKResponse[Empty]:
        """https://docs.devino.online/0.2.0/ru/http/omni/"""
        return self._client.post(
            self.create_omni_scenario_url,
            Empty,
            data=query.json(),
            headers={
                "Authorization": f"Key {self._token}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    def send_transactional_message(
        self, query: SendTransactionalMessageRequest, timeout=3
    ) -> SDKResponse[SendTransactionalMessageResponse]:
        """https://docs.devino.online/0.2.0/ru/http/omni/#sending-transactional-messages"""
        return self._client.post(
            self.send_transactional_message_url,
            SendTransactionalMessageResponse,
            data=query.json(),
            headers={
                "Authorization": f"Key {self._token}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )
