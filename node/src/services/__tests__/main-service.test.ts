import * as mainServices from "../mainService";

const mockPrinter = jest.fn((message) => `${message}-received`);

const messageResponse = "Hello world!";

describe("Main services", () => {
  it("Should return main message.", async () => {
    const service = mainServices.getMessage;

    const receivedResponse = service();

    expect(receivedResponse).toEqual(messageResponse);
  });

  it("Should call the printer service using the provided message.", async () => {
    const service = mainServices.printService;
    const expectedResults = `${messageResponse}-received`;

    service(mockPrinter, messageResponse);

    expect(mockPrinter).toHaveBeenCalled;
    expect(mockPrinter).toHaveReturnedWith(expectedResults);
  });
});
