import torch

device = torch.device("cuda" if torch.cuda.is_available() else 'cpu')

def model_train(model, train_loader):
    model.train()
    size = len(train_loader.dataset)
    batch_size = train_loader.batch_size

    for batch, (x, y) in enumerate(train_loader):
        model.optimizer.zero_grad()
        x, y = x.to(device), y.to(device)
        
        pred = model(x)
        loss = model.criterion(pred, y)
        loss.backward()
        model.optimizer.step()

        if batch % 1 == 0:
            print(f"training --> {batch_size*batch:>5d}/{size:>5d}, loss --> {loss:>5.3f}")

def model_eval(model, cv_loader):
    model.eval()

    pass

def model_test(model, test_loader):
    model.eval()

    pass